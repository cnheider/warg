#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          Plugin

           Created on 13/06/2020
           """

import sys

if sys.version_info[:2] >= (3, 10):
    # pylint: disable=no-name-in-module
    # noinspection PyProtectedMember
    from importlib.metadata import entry_points, EntryPoint
else:
    # noinspection PyProtectedMember
    from importlib_metadata import entry_points, EntryPoint

from typing import Tuple, Generator, Any

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


def get_dynamic_plugins(
    package_name: str,
) -> Generator[EntryPoint, Any, None]:
    """Returns a list specifying dynamically loaded plugins.

    Returns:
      The list of dynamic plugins.

    [1]: https://packaging.python.org/specifications/entry-points/
    """

    return (
        entry_point.load() for entry_point in entry_points(group=f"{package_name}_plugins", name=package_name)
    )


if __name__ == "__main__":
    print(get_plugins("warg"))

    print(entry_points())
