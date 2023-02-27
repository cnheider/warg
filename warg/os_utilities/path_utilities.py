#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 07-05-2021
           """

import os
import subprocess
from pathlib import Path

__all__ = ["latest_file", "exist_any_extension", "system_open_path"]

from warg.os_utilities.os_platform import is_windows, is_mac, has_x_server


def system_open_path(path: Path, *, verbose: bool = False) -> None:
    """
    Use system defaults for opening path/uris

    :param path:
    :type path:
    :param verbose:
    :type verbose:
    :return:
    :rtype:
    """
    if has_x_server():
        if verbose:
            print(f"Opening the directory ({path}) using the systems default file manager")

        directory = str(path)

        if is_windows():
            subprocess.Popen(["start", directory], shell=True)

        elif is_mac():
            subprocess.Popen(["open", directory])

        else:
            # try:
            subprocess.Popen(["xdg-open", directory])
            # except OSError:
    else:
        print("Target display not set")


def latest_file(
    directory: Path,
    extension: str = "",
    *,
    recurse: bool = False,
    raise_on_failure: bool = True,
) -> Path:
    """

    :param directory:
    :param extension:
    :param recurse:
    :param raise_on_failure:
    :return:
    """
    a = f"*{extension}"
    if recurse:
        path_gen = directory.rglob(a)
    else:
        path_gen = directory.glob(a)
    list_of_files = list(path_gen)
    if len(list_of_files) == 0:
        msg = f"Found no previous files with extension {extension} in {directory}"
        if raise_on_failure:
            raise FileNotFoundError(msg)
        print(f"{msg}, returning None!")
        return
    return max(list_of_files, key=os.path.getctime)  # USES CREATION TIME


def exist_any_extension(p: Path) -> bool:
    """
    If any file with that stem exist in parent directory, return True.

    :param p:
    :type p:
    :return:
    :rtype:
    """
    for _ in p.parent.glob(f"{p.stem}.*"):
        return True
    return False


if __name__ == "__main__":
    print(latest_file(Path(__file__).parent, recurse=True))
    print(exist_any_extension(Path(__file__)))
    print(exist_any_extension(Path.cwd() / "__init__.py"))
    print(exist_any_extension(Path.cwd() / "__init__"))
    print(exist_any_extension(Path.cwd() / "__init__.test"))
    print(exist_any_extension(Path.cwd() / "__init___.py"))
