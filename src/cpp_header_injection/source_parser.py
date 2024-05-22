import os
import re

from cpp_header_injection.logger import dev_log


INCLUDE_REGEX = re.compile(r"\n\s*#[ \t]*include[ \t]*<(?P<include>.*)>.*\n")
LINEFEED_REGEX = re.compile(r"\n")
DOUBLE_LINEFEED_REGEX = re.compile(r"\n\n")
INCLUDE_LINE_REGEX = re.compile(r"^\s*#[ \t]*include[ \t]*<(?P<include>.*)>")
SYMBOLS_IN_LINE = 80
SLASH_LINE = "//" + ("#" * (SYMBOLS_IN_LINE - 4)) + "//"


class SourceParser:
    def __init__(self, conf: dict):
        self.conf = conf
        self.inserted_includes = set()
        self.system_headers = set()
        self.out_text = ""

    def parse_src(self, src_abspath: str) -> str:
        dev_log("Starting parse_src()")
        print(src_abspath)
        # Reset values.
        self.inserted_includes = set()
        self.system_headers = set()
        self.out_text = ""

        # Parse source file.
        preproc_text = self._get_preprocessed_text(src_abspath)
        self._recursive_parse_include(preproc_text)
        text_to_insert = self._get_text_for_insert(preproc_text)
        self._add_to_out_text("SOURCE_FILE", text_to_insert)
        self._insert_system_headers()

        return self.out_text

    def _parse_include(self, include: str) -> None:
        include_abspath = self._get_include_abspath(include)
        # Check if include is system.
        if include_abspath is None:
            self.system_headers.add(include)
            return

        # Check if include is already handled.
        if include in self.inserted_includes:
            return

        # Handle include text.
        preproc_text = self._get_preprocessed_text(include_abspath)
        self._recursive_parse_include(preproc_text)
        text_to_insert = self._get_text_for_insert(preproc_text)
        self._add_to_out_text(include, text_to_insert)
        self.inserted_includes.add(include)

    def _add_to_out_text(self, file_name: str, text_to_insert: str) -> None:
        spaces = SYMBOLS_IN_LINE - len(file_name) - 4
        half = spaces // 2
        spaces_l = " " * half
        spaces_r = " " * (spaces - half)
        include_line = f"//{spaces_l}{file_name}{spaces_r}//"

        self.out_text += f"""
{SLASH_LINE}
{include_line}
{SLASH_LINE}
{text_to_insert}
"""

    def _get_include_abspath(self, include: str) -> str | None:
        """
        If include is not found, it is considered system and function
        returns None.
        """
        if os.path.isabs(include):
            return include

        for include_dir in self.conf["include_dirs"]:
            include_dir = os.path.dirname(include_dir)
            include_abspath = os.path.join(include_dir, include)
            if os.path.exists(include_abspath):
                return include_abspath

        return None

    def _get_preprocessed_text(self, file_abspath: str) -> str:
        with open(file_abspath, "r") as f:
            text = f.read()
            text = LINEFEED_REGEX.sub("\n\n", text)
            text = "\n" + text
            return text

    def _recursive_parse_include(self, preproc_text: str) -> None:
        match_iter = INCLUDE_REGEX.finditer(preproc_text)
        for match in match_iter:
            include = match.group('include')
            self._parse_include(include)

    def _get_text_for_insert(self, preproc_text: str) -> str:
        text = INCLUDE_REGEX.sub("", preproc_text)
        text = DOUBLE_LINEFEED_REGEX.sub("\n", text)
        return text

    def _insert_system_headers(self) -> None:
        headers = [f"#include <{header}>" for header in self.system_headers]
        header_block = "\n".join(headers)
        self.out_text = header_block + "\n" + self.out_text
