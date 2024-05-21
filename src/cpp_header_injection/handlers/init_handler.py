import os
from argparse import ArgumentParser
from argparse import Namespace

from cpp_header_injection.logger import dev_log
from cpp_header_injection.app_conf_funcs import create_conf_dir
from cpp_header_injection.app_conf_funcs import create_conf_file


def init_handler(args: Namespace) -> None:
    dev_log(f"init_handler is called with {args}")
    args_dict = dict(args.__dict__)
    project_root = args_dict["project_root"]

    # Create config directory.
    project_root = os.path.abspath(project_root)
    create_conf_dir(project_root)

    # Create config file.
    conf = {
        "project_root": project_root,
        "project_root_dir": os.path.basename(project_root),
        "include_dirs": [],
    }

    create_conf_file(conf)


def setup_init_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-p", "--project-root",
        required=True,
        type=str,
        help="path to project root",
    )

    parser.set_defaults(func=init_handler)
