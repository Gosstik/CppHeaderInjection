import os
from argparse import ArgumentParser
from argparse import Namespace

from cpp_header_injection.exceptions import CppHeaderInjectionException
from cpp_header_injection.logger import dev_log
from cpp_header_injection.source_parser import SourceParser

from cpp_header_injection.app_conf_funcs import get_conf
from cpp_header_injection.app_conf_funcs import get_abspath

from cpp_header_injection.exceptions import CppHeaderInjectionException


################################################################################
#                                  API                                         #
################################################################################


def run_handler(args: Namespace) -> None:
    dev_log(f"run_handler is called with {args}")
    args_dict = dict(args.__dict__)

    # Get abs path os source file.
    src_file = args_dict["source_file"]
    src_abs_file = get_abspath(src_file)
    if src_abs_file is None:
        raise CppHeaderInjectionException(
            f"can't get absolute path for '{src_file}' source_file",
        )

    # Core logic.
    conf = get_conf()
    src_parser = SourceParser(conf)
    out_text = src_parser.parse_src(src_abs_file)

    # Get path of out_file.
    out_file = args_dict["out_file"]
    if args_dict["same_dir"]:
        out_dir = os.path.dirname(src_abs_file)
        out_abs_file = os.path.join(out_dir, out_file)
    else:
        out_abs_file = os.path.abspath(out_file)

    # Write to out_file.
    with open(out_abs_file, "w") as f:
        f.write(out_text)


def setup_run_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-s", "--same-dir",
        required=False,
        action="store_true",
        help="save out_file in the same dir as the source_file",
    )
    parser.add_argument(
        "source_file",
        type=str,
        help="path to source file to insert code into",
    )
    parser.add_argument(
        "out_file",
        type=str,
        help="relative path to output file",
    )

    parser.set_defaults(func=run_handler)
