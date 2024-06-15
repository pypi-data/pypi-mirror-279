# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import logging
import os
import platform
import re
import zipfile
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from typing import IO, Union

from polygraphy.backend.trt import EngineFromBytes, SaveEngine

from trt_cloud import utils


@dataclass
class TrtVersion:
    major: int
    minor: int
    patch: int

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def from_version_str(cls, version_str: str) -> 'TrtVersion':
        version_regex = re.compile(r"([0-9]+)[^\.]*\.([0-9]+)[^\.]*\.([0-9]+).*")
        version_components = version_regex.findall(version_str)

        if not version_components or not len(version_components[0]) == 3:
            raise ValueError("Failed to Parse TRT Version")

        return TrtVersion(
            major=int(version_components[0][0]),
            minor=int(version_components[0][1]),
            patch=int(version_components[0][2])
        )


class RefitHelper:
    @classmethod
    def _validate_file_path(cls, file_path: str):
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise ValueError(f"Invalid path {file_path}")

    @classmethod
    def _check_file_ext(cls, file_path: str, expected_extension: str) -> bool:
        filename, file_ext = os.path.splitext(os.path.basename(file_path))
        return file_ext == expected_extension

    def _read_trt_engine_version(self, engine_file: IO[bytes]) -> TrtVersion:
        engine_metadata = engine_file.read(28)
        engine_file.seek(0)

        if not engine_metadata or len(engine_metadata) < 28:
            raise ValueError("Failed to read trt version from engine file")

        try:
            # Byte 27 has the last version digit.
            return TrtVersion(
                major=int(engine_metadata[24]),
                minor=int(engine_metadata[25]),
                patch=int(engine_metadata[26])
            )
        except Exception:
            raise ValueError("Failed to read trt version from engine file")

    def _import_trt_runtime(self, is_engine_vc: bool) -> Union['tensorrt_lean', 'tensort']:  # noqa
        if is_engine_vc:
            import tensorrt_lean as trt
        else:
            import tensorrt as trt

        return trt

    def _validate_tensorrt_import(self, engine_tensorrt_version: TrtVersion, is_engine_vc: bool):
        tensorrt_python_package_name = "tensorrt-lean" if is_engine_vc else "tensorrt"

        try:
            trt = self._import_trt_runtime(is_engine_vc)
            try:
                installed_trt_version = TrtVersion.from_version_str(trt.__version__)
            except Exception:
                logging.warning(f"Failed to determine currently installed {tensorrt_python_package_name} version."
                                " Will attempt to continue. If you run into errors,"
                                f" please install {tensorrt_python_package_name} version {engine_tensorrt_version},"
                                f" or another compatible version.")
                return

            if installed_trt_version != engine_tensorrt_version:
                logging.warning(
                    f"Currently installed {tensorrt_python_package_name} version {installed_trt_version}"
                    f" is not the same as the version"
                    f" the engine was built with ({engine_tensorrt_version})."
                    f" Will attempt to continue. If you run into"
                    f" errors, please install {tensorrt_python_package_name} {engine_tensorrt_version}"
                    f" or another compatible version."
                )

        except ImportError:
            raise RuntimeError(
                f"Unable to import {tensorrt_python_package_name}. "
                f"To be able to refit the engine, please install {tensorrt_python_package_name}"
                f" version {engine_tensorrt_version}"
            )

    def _load_engine(self, engine_path: str, is_engine_vc: bool) -> 'tensorrt.ICudaEngine':  # noqa
        self._validate_file_path(engine_path)
        if self._check_file_ext(engine_path, ".zip"):
            with zipfile.ZipFile(engine_path) as build_result_zip:
                if "build_result/engine.trt" not in build_result_zip.namelist():
                    raise ValueError(f"{engine_path} does not contain a TRT engine (build_result/engine.trt)")

                with build_result_zip.open("build_result/engine.trt") as trt_engine:
                    try:
                        engine_trt_version = self._read_trt_engine_version(trt_engine)
                    except Exception:
                        raise RuntimeError(f"Failed to read TRT version from engine: {engine_path}")

                    self._validate_tensorrt_import(engine_trt_version, is_engine_vc)
                    return EngineFromBytes(trt_engine.read())()

        else:
            with open(engine_path, "rb") as trt_engine:
                try:
                    engine_trt_version = self._read_trt_engine_version(trt_engine)
                except Exception:
                    raise RuntimeError(f"Failed to read TRT version from engine: {engine_path}")

                self._validate_tensorrt_import(engine_trt_version, is_engine_vc)
                return EngineFromBytes(serialized_engine=trt_engine.read())()

    def _refit_engine(self, trt_engine: 'tensorrt.ICudaEngine',  # noqa
                      onnx_model_path: str, is_engine_vc: bool) -> 'tensorrt.ICudaEngine':  # noqa
        self._validate_file_path(onnx_model_path)
        with TemporaryDirectory() as tmpdir:
            if self._check_file_ext(onnx_model_path, ".onnx"):
                refit_input_onnx = onnx_model_path
            elif self._check_file_ext(onnx_model_path, ".zip"):
                refit_input_onnx = utils.extract_onnx_file(tmpdir, onnx_model_path)
            else:
                raise ValueError(f"{onnx_model_path} does not appear to be a .onnx or a .zip file.")

            trt = self._import_trt_runtime(is_engine_vc)
            trt_logger = trt.Logger()
            trt_refitter = trt.Refitter(trt_engine, trt_logger)
            onnx_refitter = trt.OnnxParserRefitter(trt_refitter, trt_logger)
            if not onnx_refitter.refit_from_file(refit_input_onnx):
                raise RuntimeError(f"Failed to refit from model {onnx_model_path}")
            if not trt_refitter.refit_cuda_engine():
                raise RuntimeError("Failed to refit cuda engine")

        return trt_engine

    def _save_refitted_engine(self, refitted_engine: 'tensorrt.ICudaEngine', output_path: str):  # noqa
        dir_tree = os.path.dirname(os.path.abspath(output_path))
        if not os.path.exists(dir_tree):
            logging.info(f"Creating {dir_tree}")
            os.makedirs(dir_tree, exist_ok=True)

        SaveEngine(refitted_engine, output_path)()

    def refit(self, engine_path: str, onnx_model_path: str, output_path: str, is_engine_vc: bool = False):
        if platform.system() == "Darwin":
            raise OSError("Darwin based operating system not supported for refit.")

        if is_engine_vc:
            logging.info("Engine is VC. Will use lean runtime to refit.")

        self._save_refitted_engine(
            refitted_engine=self._refit_engine(
                trt_engine=self._load_engine(engine_path, is_engine_vc),
                onnx_model_path=onnx_model_path,
                is_engine_vc=is_engine_vc
            ),
            output_path=output_path
        )
