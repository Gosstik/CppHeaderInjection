import json
from argparse import ArgumentParser
from argparse import Namespace

from cpp_header_injection.logger import dev_log
from cpp_header_injection.app_conf_funcs import get_conf
from cpp_header_injection.app_conf_funcs import add_include_dirs
from cpp_header_injection.app_conf_funcs import remove_include_dirs


def config_handler(args: Namespace) -> None:
    dev_log(f"config_handler is called with {args}")
    args_dict = dict(args.__dict__)

    # Handle args.
    add_dirs = args_dict["add_include_dir"]
    if add_dirs is not None:
        if isinstance(add_dirs, str):
            # TODO: allow multiple args
            add_dirs = [add_dirs]
        add_include_dirs(add_dirs)

    remove_dirs = args_dict["remove_include_dir"]
    if remove_dirs is not None:
        if isinstance(remove_dirs, str):
            # TODO: allow multiple args
            remove_dirs = [remove_dirs]
        remove_include_dirs(remove_dirs)

    list_conf = args_dict["list"]
    if list_conf:
        conf = get_conf()
        conf_str = json.dumps(conf, indent=2, ensure_ascii=False)
        print(conf_str, flush=True)


def setup_config_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-a", "--add-include-dir",
        required=False,
        type=str,
        action="append",
        help="add path to directory from where headers are included",
    )
    parser.add_argument(
        "-r", "--remove-include-dir",
        required=False,
        type=str,
        help="remove path to directory from where headers are included",
    )
    parser.add_argument(
        "-l", "--list",
        required=False,
        action="store_true",
        help="list current config",
    )

    parser.set_defaults(func=config_handler)
