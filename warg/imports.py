#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 28/06/2020
           """

from importlib.util import find_spec
from warnings import warn

__all__ = ["is_module_available", "import_warning", "reimported_warning"]


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
        warn(f"You have imported {module_name}")


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

    def main():

        mod = "matplotlib"
        import_warning(mod)
        from matplotlib import pyplot

        import_warning(mod)
        pyplot.figure()

    main()
