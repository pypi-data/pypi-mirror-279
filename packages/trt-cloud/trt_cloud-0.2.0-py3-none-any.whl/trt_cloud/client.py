# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import datetime
import json
import logging
import os
import shutil
import sys
import time
import zipfile
from dataclasses import asdict, dataclass
from fnmatch import fnmatch
from tempfile import TemporaryDirectory
from typing import List

from trt_cloud import constants, utils
from trt_cloud.ngc_registry import NGCRegistryClient
from trt_cloud.nvcf import NVCFClient
from trt_cloud.polygraphy_helper import (PolyGraphyCallResult, PolygraphyTool,
                                         PolygraphyToolHelper)
from trt_cloud.refitter.refit_helper import RefitHelper
from trt_cloud.state import NVCFAssetCache, TRTCloudConfig
from trt_cloud.versions import BuilderFunction, parse_versions_from_functions


class BuilderFunctionException(Exception):
    """
    Exception which is raised when a Builder Function returns an error response.
    """
    pass


class PrintMessageOnCtrlC:
    """
    Context manager which prints a message if it receives a KeyboardInterrupt.
    """
    def __init__(self, msg, level=logging.INFO):
        self.msg = msg
        self.level = level

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == KeyboardInterrupt:
            logging.log(self.level, "\n" + self.msg)


class PrintNewlineOnExit:
    """
    Context manager which prints a new line on exit.
    Useful for printing the missing newline after "Latest poll status".
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        print("")

@dataclass
class PrebuiltEngine:
    """
    A class representing a TRT engine (or multidevice engines)
    which can be downloaded from NGC.
    """
    model_name: str
    version_name: str

    @property
    def id(self):
        return f"{self.model_name}:{self.version_name}"

    trtllm_version: str = None
    os: str = "Unknown"
    cpu_arch: str = "Unknown"
    gpu: str = "Unknown"
    num_gpus: int = -1
    max_batch_size: int = -1
    download_size: str = "Unknown"
    download_size_bytes: int = 0
    weight_stripped: bool = False
    other_attributes: dict = None

    def __post_init__(self):
        self.download_size = f"{self.download_size_bytes/1e6:.2f} MB"

    @classmethod
    def from_attributes(cls, model_name: str, version_name: str, attributes: dict) -> 'PrebuiltEngine':
        attrs = attributes.copy()
        return PrebuiltEngine(
            model_name=model_name,
            version_name=version_name,
            trtllm_version=attrs.pop("trtllm_version", "Unknown"),
            os=attrs.pop("os", "Unknown"),
            cpu_arch=attrs.pop("cpu_arch", "Unknown"),
            gpu=attrs.pop("gpu", "Unknown"),
            num_gpus=int(attrs.pop("num_gpus", -1)),
            max_batch_size=int(attrs.pop("max_batch_size", -1)),
            download_size_bytes=attrs.pop('download_size', 0),
            weight_stripped=(str(attrs.pop("weightless", "False")).lower() == "true"
                             or str(attrs.pop("weight_stripped", "False")).lower() == "true"),
            other_attributes=attrs
        )

    def as_pretty_print_dict(self, include_all_headers=True):
        ret = asdict(self)
        ret["other_attributes"] = self.other_attributes or ""

        if not include_all_headers:
            del ret["cpu_arch"]
            del ret["max_batch_size"]
            del ret["download_size_bytes"]
            del ret["other_attributes"]
        return ret


class TRTCloud:
    """
    A client for building and downloading TRT Cloud inference engines.
    """

    def __init__(self):
        self.config = TRTCloudConfig()
        self.ngc_registry = NGCRegistryClient(
            ngc_endpoint=os.environ.get("NGC_ENDPOINT"),
            auth_endpoint=os.environ.get("NGC_AUTH_ENDPOINT"),
            ngc_org=utils.get_ngc_model_org(),
            ngc_team=utils.get_ngc_model_team(),
        )

        self._nvcf_client = None
        self.asset_cache = NVCFAssetCache()
        self.polygraphy_helper = PolygraphyToolHelper(polygraphy_tool=PolygraphyTool.SURGEON)
        self.refit_helper = RefitHelper()

    @property
    def nvcf_client(self) -> NVCFClient:
        if self._nvcf_client is None:
            # Use saved NVCF credentials.
            client_id, client_secret, nvapi_key = self.config.read_saved_login()
            self._nvcf_client = NVCFClient(
                nvcf_endpoint=os.getenv("NVCF_ENDPOINT"),
                auth_endpoint=os.getenv("NVCF_AUTH_ENDPOINT"),
                ssa_client_id=client_id,
                ssa_client_secret=client_secret,
                nvapi_key=nvapi_key
            )

        return self._nvcf_client

    def get_available_functions(self) -> List[BuilderFunction]:
        """
        Get the latest versions of available engine-building NVCF functions.
        """
        fns = self.nvcf_client.get_functions()
        return parse_versions_from_functions(fns)

    def start_onnx_build(
        self,
        onnx_model: str,
        gpu: str,
        os_name: str,
        strip_weights: bool,
        trtexec_args: List[str],
        local_refit: bool,
        out_file: str = None,
        function_id: str = None,
        function_version: str = None,
        tags: List[str] = None,
    ):
        """
        Build a TRT Engine from an ONNX model on the cloud.

        Parameters:
        onnx_model: str
            The onnx model to build into a TRT engine. Can either be the path to a local
            file, or a HTTP/HTTPS URL. If the ONNX model uses external weights, this file
            should be a ZIP containing the .onnx model along with the extrernal weight files.
        gpu: str
            The GPU model which the engine should be built for. Use `trt-cloud info` to get
            the list of available GPUs.
        os_name: str
            The name of the OS which the engine will be used on - "linux" or "windows".
        strip_weights: bool
            Strip weights from the ONNX model before uploading it to TRT Cloud. The engine
            returned by the server will be weight-stripped. After the engine is downloaded,
            it will be refit with the original weights unless 'no_refit' is True.
        trtexec_args: List[str]
            Additional command-line arguments to pass to trtexec when building the engine.
            See the user guide for the list of allowed trtexec arguments.
        local_refit: bool
            Used only when 'strip_weights' is True. If 'local_refit' is True, the downloaded engine
            will be refit locally with the original weights in the ONNX model.
        out_file: str
            File path to which the build result should be saved to.
        function_id: str
            If specified, uses this NVCF Function ID
            regardless of specified GPU, OS, and TRT Version.
        function_version: str
            If specified, uses this NVCF Function version ID
            regardless of specified GPU, OS, and TRT Version.
        tags: List[str]
            List of tags to filter available functions by.
        """

        # Select NVCF Function based on specified GPU, OS and Tags, or ID/Version.
        for nvcf_func in self.get_available_functions():
            if (
                function_id
                and function_version
                and function_id == nvcf_func.func_id
                and function_version == nvcf_func.version_id
            ) or (
                nvcf_func.os == os_name
                and nvcf_func.gpu == gpu
                and (not tags or all(tag in nvcf_func.tags for tag in tags))
            ):
                break
        else:
            missing_params = ""
            if function_id and function_version:
                missing_params = f"ID={function_id} and Version={function_version}"
            elif tags:
                missing_params = f"GPU={gpu}, OS={os_name} and Tags {tags}"
            else:
                missing_params = f"GPU={gpu}, OS={os_name}"

            error_str = f"No available function with {missing_params}."
            raise ValueError(
                f"{error_str} Please use 'trt-cloud info' to get information on available functions."
            )

        # Upload NVCF asset if necessary
        nvcf_asset_id_list = list()
        if onnx_model.startswith("http://") or onnx_model.startswith("https://"):
            if strip_weights:
                logging.warning("Skipping weight pruning for model with a url")
                if local_refit:
                    logging.warning(f"Will not locally refit {onnx_model} for model with a url. "
                                    f"Please download the model locally "
                                    f"and run the refit command after the build to refit.")
                    local_refit = False
            request_body_onnx_value = onnx_model
        elif os.path.exists(onnx_model):
            with TemporaryDirectory() as weight_strip_temp_dir, TemporaryDirectory() as weight_strip_output_dir:
                if strip_weights:
                    _, model_ext = os.path.splitext(os.path.basename(onnx_model))
                    if model_ext == ".zip":
                        weight_strip_input_onnx = utils.extract_onnx_file(weight_strip_temp_dir, onnx_model)
                    elif model_ext == ".onnx":
                        weight_strip_input_onnx = onnx_model
                    else:
                        raise ValueError(
                            f"{onnx_model} does not appear to be a .onnx or a .zip file. "
                             "Cannot prune weights from unknown file format."
                        )

                    weight_stripped_model = os.path.join(weight_strip_output_dir, "model_weightless.onnx")
                    polygraphy_call_result, polygraphy_output = self.polygraphy_helper.run([
                        "weight-strip",
                        weight_strip_input_onnx,
                        "-o", weight_stripped_model,
                    ])

                    if polygraphy_call_result == PolyGraphyCallResult.ERROR or \
                       not os.path.exists(weight_stripped_model):
                        raise RuntimeError(f"Failed to prune weights from {onnx_model} :\n{polygraphy_output}")
                    else:
                        logging.info(f"Pruned weights from {onnx_model} -> {weight_stripped_model}")

                    # Zip in case weight_strip_output_dir contains external weight files.
                    if len(os.listdir(weight_strip_output_dir)) > 1:
                        weight_stripped_model = shutil.make_archive(
                            os.path.join(weight_strip_temp_dir, "weights_stripped"),
                            'zip',
                            weight_strip_output_dir
                        )

                nvcf_asset_to_upload = weight_stripped_model if strip_weights else onnx_model
                logging.info(f"Uploading {nvcf_asset_to_upload}")

                nvcf_asset_id = self._cached_nvcf_asset_upload(nvcf_asset_to_upload)
                nvcf_asset_id_list.append(nvcf_asset_id)
                request_body_onnx_value = nvcf_asset_id
        else:
            raise FileNotFoundError(onnx_model)

        if strip_weights:
            if "--stripWeights" not in set(trtexec_args):
                logging.debug("Adding --stripWeights to trtexec args for weight-stripped engine build.")
                trtexec_args.append("--stripWeights")
        else:
            local_refit = False

        request_body = {
            "engine_build_type": "onnx",
            "engine_build_args": {
                "onnx": request_body_onnx_value,
                "trtexec_args": trtexec_args,
            }
        }

        logging.debug("Request Body: %s", request_body)

        function_id = nvcf_func.func_id
        version_id = nvcf_func.version_id

        logging.info("Selected NVCF Function %s with version %s", function_id, version_id)
        if not nvcf_func.is_latest:
            logging.warning(
                "There is a more recent function version available for this combination of GPU, OS and Tags. "
                "Use 'trt-cloud info' to get the latest available versions."
            )
        with PrintMessageOnCtrlC(
            "Interrupting the function invocation may result in the build being started "
            "without a request ID.",
            level=logging.WARNING
        ):
            nvcf_response = self.nvcf_client.call_function(
                function_id,
                version_id,
                request_body,
                nvcf_asset_id_list,
            )

        self._handle_possible_error_response(nvcf_response)

        # Possible status codes: 200, 202, 302
        if nvcf_response.status_code == 202:

            request_id = nvcf_response.headers["NVCF-REQID"]
            logging.info("NVCF Request ID: %s", request_id)

            # Continue ONNX build
            nvcf_response = self._poll_build_until_finished(request_id)

        self._save_build_result(nvcf_response, out_file,
                                refit=local_refit, refit_onnx_model_path=onnx_model,
                                is_engine_vc=("--vc" in set(trtexec_args)))

    def continue_onnx_build(
        self,
        request_id: str,
        out_file: str
    ):
        """
        Poll and download a previously-started engine build. This method is useful when
        the client was interrupted when waiting for the build to complete.

        Parameters:
        request_id: str
            The request ID of the build. The request ID is logged to the console when
            a build is started.
        out_file: str
            File path to which the build result should be saved to.
        """
        nvcf_response = self._poll_build_until_finished(request_id)
        self._save_build_result(nvcf_response, out_file,
                                refit=False, refit_onnx_model_path=None, is_engine_vc=False)

    def _poll_build_until_finished(self, request_id: str):
        """
        Poll a NVCF function status until it returns a status that is not 202.
        """

        def clear_line():
            sys.stdout.write("\r")
            sys.stdout.flush()

        with PrintMessageOnCtrlC(
            msg="Caught KeyboardInterrupt. "
            f"Build status may be queried using Request ID {request_id}."
        ), PrintNewlineOnExit():
            POLL_EVERY = 5 # seconds
            start_time = time.time() - POLL_EVERY # skip the first wait.
            status_code = 202
            queue_position = self.nvcf_client.get_request_position_in_queue(request_id)
            while status_code == 202:
                end_time = time.time()
                elapsed = end_time - start_time
                if elapsed < POLL_EVERY:
                    time.sleep(POLL_EVERY - elapsed)
                start_time = end_time

                clear_line()
                now = datetime.datetime.now().strftime('%H:%M:%S')
                sys.stdout.write(f"[I] Latest poll status: {status_code} at {now}. ")
                sys.stdout.write(f"Position in queue: {queue_position}.")
                sys.stdout.flush()

                resp = self.nvcf_client.get_request_status(request_id)
                queue_position = self.nvcf_client.get_request_position_in_queue(request_id)
                status_code = resp.status_code
                logging.debug(
                    "Polling build status... %d. Position in queue: %s",
                    status_code, queue_position
                )

                self._handle_possible_error_response(resp)

            return resp

    def _run_refit(self, engine_path: str, onnx_model_path: str, output_path: str, is_engine_vc: bool):
        try:
            logging.info(f"Refitting {engine_path} -> {output_path}")
            self.refit_helper.refit(
                engine_path=engine_path,
                onnx_model_path=onnx_model_path,
                output_path=output_path,
                is_engine_vc=is_engine_vc
            )
            logging.info(f"Refitted engine saved to {output_path}")
        except Exception as exc:
            logging.warning(f"Unable to refit engine. Please run the refit command manually:\n{exc}")

    def _save_build_result(self, nvcf_response, out_file=None,
                           refit=False, refit_onnx_model_path=None, is_engine_vc=False):
        """
        Handle a completed build given a response from NVCF.

        Either save it to a file or print out the download URL.
        """

        def get_corrected_output_filename(out_file):
            if out_file is not None:
                return out_file
            if not os.path.isfile("build_result.zip"):
                return "build_result.zip"
            i = 1
            while os.path.isfile(f"build_result_{i}.zip"):
                i += 1
            return f"build_result_{i}.zip"

        def get_refitted_output_filename(out_file):
            refit_output_dir = os.path.dirname(os.path.abspath(out_file))
            refit_file_name, _ = os.path.splitext(os.path.basename(os.path.abspath(out_file)))
            refit_output_path = os.path.join(refit_output_dir, f"{refit_file_name}_refitted.trt")

            return refit_output_path

        def peek_at_build_result(saved_zip_path):
            with zipfile.ZipFile(saved_zip_path) as zipped:
                filenames = zipped.namelist()
                for filename in filenames:
                    if os.path.basename(filename) == "build.log":
                        break
                else:
                    logging.warning(
                        "Could not find build.log in archive. Build likely failed."
                    )
                    return
                with zipped.open(filename, "r") as f:
                    lines = f.readlines()
                logging.info("Last 5 lines of build.log:\n---")
                for line in lines[-5:]:
                    logging.info("    %s", line.decode().replace("\n", ""))

        def postprocess_build_result(saved_zip_path):
            peek_at_build_result(out_file)
            logging.info("Saved build result to %s", out_file)
            if refit:
                self._run_refit(engine_path=out_file, onnx_model_path=refit_onnx_model_path,
                                output_path=get_refitted_output_filename(out_file),
                                is_engine_vc=is_engine_vc)

        out_file = get_corrected_output_filename(out_file)

        # Small build results are returned in the body.
        if nvcf_response.status_code == 200:
            with open(out_file, 'wb') as f:
                f.write(nvcf_response.content)
            postprocess_build_result(out_file)

        # Large builds are returned as a download URL.
        elif nvcf_response.status_code == 302:
            url = nvcf_response.headers['Location']
            logging.debug("Build result download URL: %s", url)

            with TemporaryDirectory() as tmpdir:
                with PrintMessageOnCtrlC(
                    msg="Caught KeyboardInterrupt. "
                        f"Build result download URL: {url}."
                ):
                    nvcf_zip_path = os.path.join(tmpdir, "nvcf_download.zip")
                    utils.download_file(url, nvcf_zip_path)

                logging.debug("Downloaded NVCF zip to %s", nvcf_zip_path)

                # Extract build from NVCF-created zip
                with zipfile.ZipFile(nvcf_zip_path, "r") as f:
                    filename = f.namelist()[0]
                    f.extract(filename)
                    shutil.move(filename, out_file)

            postprocess_build_result(out_file)

        else:
            raise ValueError(nvcf_response.status_code)

    def _cached_nvcf_asset_upload(self, filepath_to_upload: str) -> str:
        """
        Check whether the file is already stored in the NVCF Asset Cache.
        Otherwise, upload the file as a new NVCF asset.
        """
        file_hash = self.asset_cache.filehash(filepath_to_upload)
        cache = self.asset_cache.read()

        # The file was already recently uploaded.
        if file_hash in cache:
            nvcf_asset_id = cache[file_hash].nvcf_asset_id
            logging.info("NVCF asset already exists with ID %s", nvcf_asset_id)
            return nvcf_asset_id

        nvcf_asset_id = self.nvcf_client.upload_new_asset(filepath_to_upload, "model.onnx")
        logging.info("Uploaded new NVCF asset with ID %s", nvcf_asset_id)

        # Save asset ID to cache.
        cache[file_hash] = self.asset_cache.create_new_entry(nvcf_asset_id)
        self.asset_cache.write(cache)
        return nvcf_asset_id

    def _handle_possible_error_response(self, response):
        """
        If the NVCF response is an error, raise a BuilderFunctionException.
        """

        status_code: int = response.status_code

        if status_code in [200, 202, 302]:
            return

        if status_code == 400:
            raise BuilderFunctionException(
                "Build function rejected the build request with reason: \n"
                f"\t{response.json()['detail']}"
            )
        elif status_code == 422:
            # Request body was invalid.
            detail = response.json()['detail']
            detail = detail.replace("'", '"').replace("(", "[").replace(")", "]")
            try:
                errors = json.loads(detail)
                error_msg = "Build function rejected the build request with reason:"
                for error in errors:
                    error_msg += f"\n{json.dumps(error, indent=4)}"
            except json.decoder.JSONDecodeError:
                error_msg = detail
            raise BuilderFunctionException(error_msg)
        else:
            raise BuilderFunctionException(
                "Unknown response from builder function: \n"
                f"\tStatus Code: {response.status_code}"
                f"\tContent: {response.text}"
            )

    def get_prebuilt_models(self) -> List[str]:
        """
        Return the list of Deep Learning model names for which
        there are prebuilt engines available on TensorRT Cloud.
        """

        return self.ngc_registry.list_models_in_collection(
            collection_name=constants.TRTC_PREBUILT_COLLECTION_NAME)

    def get_prebuilt_engines(
        self,
        model_name: str = None,
        trtllm_version: str = None,
        os_name: str = None,
        gpu: str = None,
        glob_match_model_name: bool = True,
    ) -> List[PrebuiltEngine]:
        """
        Return the list of NVIDIA's prebuilt TensorRT engines available for download.
        """

        all_models = self.get_prebuilt_models()
        if model_name is None:
            selected_models = all_models
        else:
            if "*" in model_name or "?" in model_name or not glob_match_model_name:
                model_name_match_string = model_name
            else:
                model_name_match_string = f"{model_name}*"

            selected_models = [model for model in all_models if fnmatch(model, model_name_match_string)]

        prebuilt_engines = []

        for selected_model in selected_models:
            engines_for_model = self.ngc_registry.get_versions_for_model(
                model_name=selected_model)

            for version_name, attributes in engines_for_model.items():
                prebuilt_engine = PrebuiltEngine.from_attributes(
                    model_name=selected_model,
                    version_name=version_name,
                    attributes=attributes
                )
                if trtllm_version and trtllm_version.upper() != prebuilt_engine.trtllm_version.upper():
                    continue
                if os_name and os_name.upper() != prebuilt_engine.os.upper():
                    continue
                if gpu and gpu.upper() != prebuilt_engine.gpu.upper():
                    continue
                prebuilt_engines.append(prebuilt_engine)

        return prebuilt_engines

    def download_prebuilt_engine(self, model_name: str, version_name: str, output_filepath=None):
        """
        Download a Prebuilt TRT engine from TensorRT Cloud.
        """

        candidate_engines = self.get_prebuilt_engines(model_name=model_name, glob_match_model_name=False)
        candidate_engines = [engine for engine in candidate_engines
                             if engine.model_name == model_name and engine.version_name == version_name]

        if not candidate_engines:
            raise ValueError(f"No engine found for model '{model_name}' called '{version_name}'")

        if len(candidate_engines) > 1:
            # Shouldn't happen but just in case.
            logging.warning(f"Found multiple engines with version {version_name}.")

        if not output_filepath:
            output_filepath = f"{model_name}_{version_name}_files.zip"
        else:
            _, file_ext = os.path.splitext(os.path.basename(output_filepath))
            if file_ext == "":
                logging.warning("No file extension provided. Adding .zip extension to the downloaded file")
                output_filepath += ".zip"
            elif file_ext != ".zip":
                logging.warning(f"Output will be saved with the extension {file_ext} but will be a zip archive.")

        self.ngc_registry.download_model(
            model_name=model_name,
            model_version=version_name,
            output_path=output_filepath
        )

        return output_filepath
