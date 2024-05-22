import sys
from typing import TextIO
import cpp_header_injection.app_conf as app_conf


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def dev_log(message: str, file: TextIO = sys.stdout):
    if app_conf.DEBUG_MODE:
        print(
            f"{Color.PINK}[DEV] {message}{Color.END}",
            file=file,
            flush=True,
        )


def error_log(message: str, file: TextIO = sys.stderr):
    print(
        f"{Color.RED}[ERROR] {message}{Color.END}",
        file=file,
        flush=True,
    )


def user_log(message: str, file: TextIO = sys.stdout):
    print(
        f"[HEADER_INJECTION] {message}",
        file=file,
        flush=True,
    )


def warning_log(message: str, file: TextIO = sys.stdout):
    print(
        f"{Color.YELLOW}[WARNING] {message}{Color.END}",
        file=file,
        flush=True,
    )
