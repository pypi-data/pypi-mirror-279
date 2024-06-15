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
import math
import os
import zipfile
from functools import lru_cache
from pathlib import Path

import requests
from rich.progress import Progress

from trt_cloud.constants import (TRTC_PREBUILT_ENGINE_ORG,
                                 TRTC_PREBUILT_ENGINE_TEAM)


def download_file(
    url: str,
    output_filepath: str,
    headers: dict = None,
    quiet: bool = False
) -> str:
    response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
    if not response.ok:
        raise RuntimeError(f"Failed to download {url}", response)

    total_length = int(response.headers["Content-Length"])
    chunk_size = 2 ** 20  # 1MB

    # Create a Progress bar
    with Progress(disable=quiet) as progress:

        # Create a Task object to represent the progress of the download
        num_chunks = math.ceil(total_length / chunk_size)
        task = progress.add_task("Downloading ", total=num_chunks)

        with open(output_filepath, "wb") as output:
            for content in response.iter_content(chunk_size):
                if content:
                    output.write(content)
                    progress.update(task, advance=1)

    return output_filepath


def check_and_display_eula(license_path: str, eula_name: str, license_preamble: str = "",
                           license_path_format_string="Please find a copy of the license here: {}.") -> bool:
    if os.path.exists(license_path):
        with open(license_path, "r", encoding="utf8") as f:
            license_text = f.read()
    else:
        raise ValueError(f"{eula_name} not found. Must agree to EULA to proceed.")
    logging.info(f"{eula_name}\n{license_preamble}{license_text}"
                 f"\n{license_path_format_string.format(license_path)}\n")
    user_input = input(
        f"Do you agree to the {eula_name}? (yes/no) "
    ).lower().strip()

    user_agreed = user_input in {"y", "yes"}
    if not user_agreed:
        raise ValueError(f"You must agree to the {eula_name} to proceed.")

    return user_agreed


def extract_onnx_file(tmpdir, onnx_zip) -> str:
    with zipfile.ZipFile(onnx_zip, "r") as zip:
        zip.extractall(tmpdir)
    onnx_files_in_zip = list(Path(tmpdir).rglob('*.onnx'))
    if not onnx_files_in_zip:
        raise ValueError(f"No .onnx files found in {onnx_zip}.")
    if len(onnx_files_in_zip) > 1:
        raise ValueError(
            f"Multiple .onnx files found in archive: {onnx_files_in_zip}"
        )
    return str(onnx_files_in_zip[0])


def add_verbose_flag_to_parser(parser):
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase logging verbosity.")


@lru_cache()
def get_ngc_model_org():
    return os.environ.get("TRTC_ENGINE_ORG", "") or TRTC_PREBUILT_ENGINE_ORG


@lru_cache()
def get_ngc_model_team():
    return os.environ.get("TRTC_ENGINE_TEAM", None) or TRTC_PREBUILT_ENGINE_TEAM
