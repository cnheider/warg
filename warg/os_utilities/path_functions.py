#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 08/03/2020
           """

__all__ = ["ensure_existence", "path_rmtree", "sanitise_path", "path_join"]

import os
from itertools import cycle
from pathlib import Path
from shutil import rmtree
from typing import Iterable, Union

from warg.decorators import passes_kws_to


def path_join(*p: Union[Path, str]) -> Path:
    """
    drop-in replacement for os.path.join, returning a Path instead

    :param p: Sequence of path components to be joined
    :type p:  Union[Path,str]
    :return: Joined path
    :rtype: Path
    """
    p, *rest = p
    p = Path(p)
    for r in rest:
        p /= r
    return p


@passes_kws_to(rmtree)
def path_rmtree(path: Path, **kwargs) -> None:
    """
    asses_kws_to rmtree from shutil
    :param path:
    :type path: Path
    :param kwargs:
    :type kwargs:
    :return: None
    :rtype: None
    """
    rmtree(str(path), **kwargs)


def sanitise_path(
    path: Path,
    naughty_directory_symbols: Iterable[str] = (
        " ",
        ",",
        "<",
        ">",
        '"',
        "|",
        "?",
        "*",
        # ".",
        # ':',
    ),
    replacement_symbols: str = ("_",),
    preserve_file_suffix: bool = True,
) -> Path:
    """
    Opinionated path sanitisation

    https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file

    preserve_file_suffix: assumes any path with a suffix at the end is a file and will preserve it but still replace naughty symbols

    """

    if not path.is_dir() and preserve_file_suffix:
        file_suffix = path.suffix
    else:
        file_suffix = None

    path_str_rep = str(path)
    path_str_rep = os.path.normpath(os.path.normcase(path_str_rep))

    for n, r in zip(naughty_directory_symbols, cycle(replacement_symbols)):
        path_str_rep = path_str_rep.replace(n, r, -1)

    path_out = Path(path_str_rep)
    if file_suffix is not None:
        return path_out.with_suffix(file_suffix)
    return path_out


def ensure_existence(
    out: Union[Path, str],
    *,
    enabled: bool = True,
    declare_file: bool = False,
    overwrite_on_wrong_type: bool = False,
    force_overwrite: bool = False,
    verbose: bool = False,
    sanitisation_func: callable = sanitise_path,
) -> Path:
    """

    :param verbose:
    :type verbose:
    :param overwrite_on_wrong_type:
    :type overwrite_on_wrong_type:
    :param force_overwrite:
    :type force_overwrite:
    :param declare_file:
    :type declare_file:
    :param sanitisation_func:
    :type sanitisation_func:
    :param out:
    :type out:
    :param enabled:
    :type enabled:
    :return:
    :rtype:"""
    if enabled:
        if isinstance(out, str):
            out = Path(out)

        if sanitisation_func:
            out = sanitisation_func(out)

        if not out.parent.exists():
            if verbose:
                print("Creating parents")
            out.parent.mkdir(parents=True, exist_ok=True)

        if out.is_file() or ("." in out.name and ".d" not in out.name) or declare_file:
            if (
                out.exists()
                and (out.is_dir() or ("." not in out.name and ".d" in out.name))
                and ((declare_file and overwrite_on_wrong_type) or force_overwrite)
            ):
                if verbose:
                    print("Removing tree")
                path_rmtree(out)
            if out.is_file() and not out.exists():
                out.touch(exist_ok=True)
        else:
            if (
                out.exists()
                and out.is_file()
                and ((not declare_file and overwrite_on_wrong_type) or force_overwrite)
            ):
                if verbose:
                    print("Deleting file")
                out.unlink()  # missing_ok=True)
            if not out.exists():
                out.mkdir(parents=True, exist_ok=True)

    return out


if __name__ == "__main__":

    def main():
        """description"""
        ensure_existence(Path.cwd() / "exclude", force_overwrite=True)
        ensure_existence(Path.cwd() / "exclude" / "0.log")
        ensure_existence(Path.cwd() / "exclude" / "log.d")
        ensure_existence(Path.cwd() / "exclude" / "log.d" / "log.a")

        # from apppath import PROJECT_APP_PATH

        # ensure_existence(PROJECT_APP_PATH.user_log / "exclude" / "log.d" / "log.a")

        def recurse_test():
            """description"""
            ensure_existence(Path.cwd() / "exclude" / "spodakjioj" / "log.d" / "log.a")
            ensure_existence(Path.cwd() / "exclude" / "spodakjioj" / "log.d" / "log.csv")

        recurse_test()

    def clean_naughty_file() -> None:
        """
        :rtype: None
        """
        pa = Path.cwd() / "uhas.asudh ojas.a." / "....  a -." / "   b.ci"

        print(pa, sanitise_path(pa))

    def clean_naughty_dir() -> None:
        """
        :rtype: None
        """
        pa = Path.cwd() / "uhas.asudh ojas.a." / "....  a -." / "   bci"

        print(pa, sanitise_path(pa))

    clean_naughty_file()
    clean_naughty_dir()
    # main()
