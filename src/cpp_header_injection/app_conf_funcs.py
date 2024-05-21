import os
import json
from typing import TextIO

import cpp_header_injection.app_conf as app_conf
from cpp_header_injection.exceptions import CppHeaderInjectionException
from cpp_header_injection.logger import dev_log
from cpp_header_injection.logger import user_log
from cpp_header_injection.logger import warning_log


def _search_conf_dir() -> str:
    if app_conf.CACHE_CONFIG_DIR != "":
        return app_conf.CACHE_CONFIG_DIR

    dev_log(f"_search_conf_dir recursive")
    cwd = os.getcwd()
    next_path = os.path.abspath(cwd)
    while True:
        cur_path = next_path
        next_path = os.path.dirname(cur_path)
        conf_dir = os.path.join(cur_path, app_conf.CONFIG_DIR_NAME)
        # dev_log(f"cur_path = {cur_path}")
        # dev_log(f"next_path = {next_path}")

        if cur_path == next_path:
            raise CppHeaderInjectionException("config directory is not found")

        if os.path.exists(conf_dir) and os.path.isdir(conf_dir):
            app_conf.CACHE_CONFIG_DIR = str(conf_dir)
            return app_conf.CACHE_CONFIG_DIR


def _get_conf_file() -> str:
    conf_dir = _search_conf_dir()
    res = os.path.join(conf_dir, app_conf.CONFIG_FILE_NAME)
    return res


def _parse_conf_file(conf_file: str) -> dict:
    with open(conf_file, "r") as f:
        res = json.load(f)
    return res


def _open_conf_file(mode: str) -> TextIO:
    conf_file = _get_conf_file()
    return open(conf_file, mode)


def _try_abspath_from_cwd(path) -> str:
    if not os.path.exists(path):
        return ""
    res = str(os.path.abspath(path))
    return res


def _try_abspath_from_project_root(path: str) -> str:
    conf = get_conf()
    project_root = conf["project_root"]
    res_path = os.path.join(project_root, path)
    if not os.path.exists(res_path):
        return ""
    res = str(os.path.abspath(path))
    return res

################################################################################
#                                  API                                         #
################################################################################


def get_abspath(path: str):
    if os.path.isabs(path):
        # Bring path to common format (note final slashes).
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise CppHeaderInjectionException(
                f"get_abspath failed: path = {path}",
            )
        return path

    res = _try_abspath_from_cwd(path)
    if len(res) != 0:
        return res

    res = _try_abspath_from_project_root(path)
    if len(res) != 0:
        raise CppHeaderInjectionException(f"Path does not exist: {path}")


def get_conf() -> dict:
    conf_file = _get_conf_file()
    with open(conf_file, "r") as f:
        res = json.load(f)
    return res


def write_conf(
        conf: dict,
        conf_fd=None,  # created file if it does not exist
) -> None:
    dev_log(f"Starting write_conf()")
    if conf_fd is None:
        conf_fd = _open_conf_file("w")
    json.dump(conf, conf_fd, indent=2, ensure_ascii=False, sort_keys=True)
    dev_log(f"Finishing write_conf()")


def create_conf_dir(project_root: str) -> None:
    conf_dir = os.path.join(project_root, app_conf.CONFIG_DIR_NAME)
    if os.path.exists(conf_dir):
        stat = input(
            f"Config directory `{conf_dir}` already exists.\n"
            f"Overwrite? [y/n] "
        )
        while True:
            if stat == "y":
                break
            if stat == "n":
                user_log("Exiting without changes.")
                raise CppHeaderInjectionException("")
            stat = input("Enter 'y' or 'n': ")

    os.makedirs(conf_dir, exist_ok=True)
    app_conf.CACHE_CONFIG_DIR = conf_dir


def create_conf_file(conf: dict) -> None:
    write_conf(conf)


def add_include_dirs(dirs: list[str]) -> None:
    conf = get_conf()
    project_root = conf["project_root"]
    root_dir = conf["project_root_dir"]
    for folder in dirs:
        if os.path.isabs(folder):
            if not os.path.exists(folder):
                warning_log(f"directory '{folder}' does not exist.")
                continue
            if folder.startswith(project_root):
                folder = folder[len(project_root) + 1:]
        if folder.startswith(root_dir):
            folder = folder[len(root_dir) + 1:]

        dev_log("project_root: {}".format(project_root))
        dev_log("folder: {}".format(folder))
        abs_folder = os.path.join(project_root, folder)
        dev_log("abs_folder: {}".format(abs_folder))
        if not os.path.exists(abs_folder):
            warning_log(f"abs_folder '{abs_folder}' does not exist, skipping")
            continue
        if folder not in conf["include_dirs"]:
            conf["include_dirs"].append(folder)
        else:
            warning_log(f"directory '{folder}' was already inserted")

    write_conf(conf)


def remove_include_dirs(dirs: list[str]) -> None:
    conf = get_conf()
    project_root = conf["project_root"]
    root_dir = conf["project_root_dir"]
    for folder in dirs:
        if folder.startswith(project_root):
            folder = folder[len(project_root) + 1:]
        if folder.startswith(root_dir):
            folder = folder[len(root_dir) + 1:]
        if folder in conf["include_dirs"]:
            conf["include_dirs"].remove(folder)
        else:
            warning_log(f"config does not contain '{folder}' directory")

    write_conf(conf)
