from argparse import ArgumentParser
from argparse import Namespace

from cpp_header_injection.handlers.init_handler import setup_init_parser
from cpp_header_injection.handlers.config_handler import setup_config_parser
from cpp_header_injection.handlers.run_handler import setup_run_parser

from cpp_header_injection.exceptions import CppHeaderInjectionException
from cpp_header_injection.logger import error_log


def parse_args() -> Namespace:
    # Configure
    parser = ArgumentParser(
        prog="header-injection",
        description="Insert code from headers into source file",
    )

    subparsers = parser.add_subparsers(help="header-injection help")
    subparsers.required = True

    init_parser = subparsers.add_parser("init", help="init help")
    setup_init_parser(init_parser)

    config_parser = subparsers.add_parser("config", help="config help")
    setup_config_parser(config_parser)

    run_parser = subparsers.add_parser("run", help="run help")
    setup_run_parser(run_parser)

    # Parse
    # parsed_args = parser.parse_args([
    #     "init",
    #     "-p",
    #     "/home/ownstreamer/Code/Python/CppHeaderInjection",
    # ])
    # parsed_args.func(parsed_args)
    #
    # parsed_args = parser.parse_args([
    #     "config",
    #     "-a",
    #     "/home/ownstreamer/Code/Python/CppHeaderInjection/tests/data/include",
    # ])
    # parsed_args.func(parsed_args)
    #
    # parsed_args = parser.parse_args([
    #     "config",
    #     "-a",
    #     "/home/ownstreamer/Code/Python/CppHeaderInjection/tests/data/other_dir/include",
    # ])
    # parsed_args.func(parsed_args)
    #
    # parsed_args = parser.parse_args([
    #     "run",
    #     "-s",
    #     "/home/ownstreamer/Code/Python/CppHeaderInjection/tests/data/main.cpp",
    #     "output.cpp",
    # ])
    # parsed_args.func(parsed_args)
    # res = parsed_args

    res = parser.parse_args()
    return res


def main():
    parsed_args = parse_args()
    parsed_args.func(parsed_args)


def main_cli():
    try:
        main()
    except CppHeaderInjectionException as e:
        log_str = str(e)
        if len(log_str) > 0:
            error_log(log_str)
        exit(0)


if __name__ == "__main__":
    main_cli()
