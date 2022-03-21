#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          Plugin

           Created on 13/06/2020
           """

from typing import Tuple

import pkg_resources

__all__ = ["get_plugins", "get_static_plugins", "get_dynamic_plugins"]


def get_plugins(package_name: str) -> Tuple:
    """Returns a list specifying all known plugins.

    This includes both first-party, statically bundled plugins and
    dynamic plugins.

    Returns:
      The list of default first-party plugins.
    """
    return (*get_static_plugins(package_name), *get_dynamic_plugins(package_name))


def get_static_plugins(package_name: str) -> Tuple:
    """Returns a list specifying  default first-party plugins.

      DECLARE GLOBAL (PACKAGE_NAME)_PLUGINS tuple with entries

    Returns:
      The list of default first-party plugins.

    """
    v = f"{package_name.upper()}_PLUGINS"
    if v in globals():
        return globals()[v][:]
    return ()


def get_dynamic_plugins(package_name: str) -> Tuple:
    """Returns a list specifying  dynamically loaded plugins.

    Returns:
      The list of dynamic plugins.

    [1]: https://packaging.python.org/specifications/entry-points/
    """

    # .load() method to import and load that entry point (module or object).
    # from importlib import metadata # new method!
    # return [      entry_point.load()      for entry_point in metadata.entry_points()[f'{package_name}_plugins']      ]
    return (entry_point.load() for entry_point in pkg_resources.iter_entry_points(f"{package_name}_plugins"))


if __name__ == "__main__":
    print(get_plugins("warg"))
