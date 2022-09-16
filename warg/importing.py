#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 28/06/2020
           """

__all__ = [
    "is_module_available",
    "import_warning",
    "reimported_warning",
    "ensure_in_sys_path",
    "clean_sys_path",
    "import_file",
]

import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Optional, Any
from warnings import warn


def import_file(path: Path, from_list=None) -> Any:
    """Import a module given its filename, works both on absolute and relative paths"""
    if from_list is None:
        from_list = {}
    globals_ = {}  # globals() # determines package context
    locals_ = {}  # locals() # Should not be used in import anyway

    sys_path = sys.path  # Save original sys.path
    try:
        sys.path.insert(0, str(path.parent.absolute()))  # Temporarily add parent dir of path to parent
        return __import__(
            path.stem, globals=globals_, locals=locals_, fromlist=from_list, level=0
        )  # Get the module name (no extension)
    finally:
        sys.path = sys_path  # Restore original sys.path


def clean_sys_path() -> None:
    """
    Clean the sys.path for dead paths or duplicates
    """
    out = []
    for path in sys.path:
        p = Path(path).resolve()
        if p.exists():
            if p not in out:
                out.append(p)

    sys.path[:] = [str(o.absolute()) for o in out]


def ensure_in_sys_path(
    path: Path, position: Optional[int] = None, resolve: bool = False, absolute: bool = True
) -> None:
    """

    Ensures that a path is in sys.path, but avoids duplicates.
    Can also resolve and absolute paths for duplication.
    Does not clean the existing paths in sys.path

    :param path:
    :type path:
    :param position:
    :type position:
    :param resolve:
    :type resolve:
    :param absolute:
    :type absolute:
    :return:
    :rtype:
    """

    if absolute:
        path = path.absolute()

    str_path = str(path)
    sys_path_snapshot = sys.path
    inclusion_test = None

    if resolve:
        sys_path_snapshot = [Path(p).resolve() for p in sys_path_snapshot]
        inclusion_test = path.resolve() in sys_path_snapshot
    else:
        inclusion_test = str_path in sys_path_snapshot

    if not inclusion_test:
        if position:
            sys.path.insert(position, str_path)
        else:
            sys.path.append(str_path)


def is_module_available(module: str) -> bool:
    """**Return True if module is available.**

    Parameters
    ----------
    module: str
          Name of the module to be checked.

    Returns
    -------
    bool
          True if installed.
    """
    return find_spec(module) is not None


def import_warning(module_name: str) -> None:
    """
    Inform the user that module has been imported,
    useful when repeated imports are heavy in the contexts of multiprocessing.
    Lets the user identify which file is reporting heavy loading and restructure code to avoid repeated importing

    :param module_name:
    :return:
    """
    from sys import modules

    if module_name in modules:
        warn(
            f"You already {module_name} had imported, consider restructuring your code to avoid repeated imports"
        )


def reimported_warning(module_name: str) -> None:
    """
    Just an idea

    :return:
    """
    raise NotImplemented
    # TODO: touch .lock file to system for module_name for a multiprocess warning if already exists,
    # delete it again once process is done?
    # context_wrapper maybe useful


if __name__ == "__main__":

    def _main() -> None:
        """
        :rtype: None
        """
        mod = "matplotlib"
        import_warning(mod)
        from matplotlib import pyplot

        import_warning(mod)
        pyplot.figure()

    def aisjdi():
        from copy import deepcopy

        s = deepcopy(sys.path)
        ensure_in_sys_path(Path(__file__).parent)
        s2 = sys.path
        print(s == s2, set(s2) - set(s), set(s) - set(s2), s2)

    def iajsd():
        from copy import deepcopy

        s = deepcopy(sys.path)
        clean_sys_path()
        s2 = sys.path
        print(s == s2, set(s2) - set(s), set(s) - set(s2), s2)

    # _main()
    # aisjdi()
    iajsd()
