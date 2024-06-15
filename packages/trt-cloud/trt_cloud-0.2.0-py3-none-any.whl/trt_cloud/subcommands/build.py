# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import argparse
import logging
import os.path
from argparse import ArgumentParser
from typing import List

from trt_cloud.client import TRTCloud
from trt_cloud.subcommands.base_subcommand import Subcommand


class BuildSubcommand(Subcommand):

    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds the 'build' subcommand to the main CLI argument parser.
        """
        build_subcommand = subparsers.add_parser(subcommand_name, help="Build a TRT engine on the cloud.")

        input_group = build_subcommand.add_mutually_exclusive_group(required=True)
        input_group.add_argument("--onnx", help="URL or local filepath of ONNX model.")
        input_group.add_argument("--request-id", help="""
            Request ID of a previously-started build.
            May only be provided if the build status has not already been reported as finished.
        """)

        # Valid for 'build --onnx' commands
        build_subcommand.add_argument(
            "--tag",
            help="""\
                                      Tags to filter the runners by (can be specified multiple times); \
                                      please run 'trt-cloud info' for a list of available runners and their tags.\
                                      """,
            dest="tags",
            nargs="*",
            default=[],
        )
        build_subcommand.add_argument("--gpu", help="GPU model to build engine for")
        build_subcommand.add_argument(
            "--os", help="OS to build engine for", choices=["linux", "windows"]
        )
        build_subcommand.add_argument(
            "--function-id", "--function", help=argparse.SUPPRESS
        )
        build_subcommand.add_argument(
            "--function-version", "--function-version-id", help=argparse.SUPPRESS
        )
        build_subcommand.add_argument("--strip-weights", action='store_true',
                                      help="Build a weight-stripped engine. "
                                           "This will prune weights from the model locally before uploading "
                                           "(unless the model is a from a url), "
                                           "and build a weight-stripped TensorRT engine.")
        build_subcommand.add_argument(
            "--local-refit", action='store_true',
            help="If set, will locally refit a weight-stripped engine after build. "
                 "Please make sure that your python environment has the TensorRT "
                 "version corresponding to the engine built."
        )
        build_subcommand.add_argument("--trtexec-args", type=str, help="Args to pass to trtexec")

        # Valid for all 'build' commands
        build_subcommand.add_argument("-o", "--out", type=str, help="File path to save the build result to.")

        return build_subcommand

    def run(self, args):
        """
        Execute the 'build' subcommand with the given args.

        The 'build' subcommand is used to start a new engine build, or to resume
        a previously-started build.

        Raises ValueError if args are invalid.
        """
        trtcloud_client = TRTCloud()
        tags = args.tags

        # OS and GPU can be specified either as args (eg. `--arg_name value`), or as tags (eg. `--tag arg_name=value`);
        # Check if there are any conflicts, and always move them to args to avoid having to check in both places
        for arg_name in ("os", "gpu"):
            arg_tag_idx = next(
                (
                    tag_idx
                    for tag_idx, tag in enumerate(tags)
                    if tag.startswith(f"{arg_name}=")
                ),
                None,
            )
            # Compare the arg (--arg_name) and tag (--tag arg_name=) versions to ensure they match,
            # and always move the tag version to the args.
            if arg_tag_idx is not None:
                arg_value = getattr(args, arg_name, None)
                arg_tag_value = tags.pop(arg_tag_idx).split("=", 1)[1]

                # Only tag is specified: move it to the args
                if arg_value is None:
                    setattr(args, arg_name, arg_tag_value)

                elif arg_value != arg_tag_value:
                    raise ValueError(
                        f"Conflicting parameters '--{arg_name}={arg_value}' and '--tag {arg_name}={arg_tag_value}'"
                    )

        # If neither `--os` nor `--tag os=` was specified, default to Linux
        if not args.os:
            args.os = "linux"

        if args.onnx:
            # Validate args
            if bool(args.function_id) != bool(args.function_version):
                raise ValueError(
                    "Both args are required when either one is used: --function-id and --function-version"
                )

            elif not args.gpu and not args.function_id and not args.function_version:
                raise ValueError("The following arg is required: --gpu")

            trtexec_args: List[str] = [arg for arg in (args.trtexec_args or "").split(" ") if arg]

            if args.local_refit and not args.strip_weights:
                raise ValueError("--local-refit is only applicable for builds with --strip-weights")

            output_file = args.out
            if output_file is not None:
                filename, ext = os.path.splitext(output_file)
                if ext and ext != ".zip":
                    logging.warning(f"The output path {output_file} has the"
                                    f" extension {ext}, but will be a zip archive")
                elif not ext:
                    output_file = f"{filename}.zip"
                    logging.info(f"Output path {filename} does not include an extension, will save as {output_file}")

            # Start a new ONNX build.
            trtcloud_client.start_onnx_build(
                onnx_model=args.onnx,
                gpu=args.gpu,
                os_name=args.os,
                strip_weights=args.strip_weights,
                local_refit=args.local_refit,
                trtexec_args=trtexec_args,
                out_file=output_file,
                function_id=args.function_id,
                function_version=args.function_version,
                tags=tags
            )

        elif args.request_id:
            for arg in ["gpu", "weightless", "skip_local_refit", "trtexec_args",
                        "function_id", "function_version"]:
                if getattr(args, arg):
                    raise ValueError(f"'{arg}' cannot be provided with --request-id")
            if args.os != "linux":
                raise ValueError("--os cannot be provided with --request-id.")

            # Continue from a NVCF request ID.
            trtcloud_client.continue_onnx_build(
                request_id=args.request_id,
                out_file=args.out
            )

        else:
            # argparse should prevent this.
            raise NotImplementedError()
