import re
from typing import TextIO
import os

from more_itertools import peekable


INCLUDE_REGEX = re.compile(r"\n\s*#[ \t]*include[ \t]*<(?P<include>.*)>.*\n")
LINEFEED_REGEX = re.compile(r"\n")
DOUBLE_LINEFEED_REGEX = re.compile(r"\n\n")
INCLUDE_LINE_REGEX = re.compile(r"^\s*#[ \t]*include[ \t]*<(?P<include>.*)>")


def read_includes():
    with open(
            os.path.join(os.path.dirname(__file__), "data", "main.cpp"),
            "r"
    ) as f:
        text = f.read()
        text = LINEFEED_REGEX.sub("\n\n", text)
        match_iter = INCLUDE_REGEX.finditer(text)
        match_iter = peekable(match_iter)
        if not match_iter:
            print("Empty...")
        for match in match_iter:
            include = match.group('include')
            print(f"include = {include}")

        text = DOUBLE_LINEFEED_REGEX.sub("\n", text)


def replace_includes():
    with open(
            os.path.join(os.path.dirname(__file__), "data", "main.cpp"),
            "r"
            ) as f:
        text = f.read()
        text = LINEFEED_REGEX.sub("\n\n", text)
        text = "\n" + text
        match_iter = INCLUDE_REGEX.finditer(text)
        match_iter = peekable(match_iter)
        if not match_iter:
            print("Empty...")
        for match in match_iter:
            include = match.group('include')
            print(f"include = {include}")

        text = INCLUDE_REGEX.sub("", text)
        text = DOUBLE_LINEFEED_REGEX.sub("\n", text)
        print("----------")
        print(text)


if __name__ == "__main__":
    replace_includes()
