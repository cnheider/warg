#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 04-01-2021
           """

import enum
import sys

__all__ = [
    "get_backend_module",
    "is_py3",
    "get_system",
    # "set_system",
    "SystemEnum",
]

from types import ModuleType

if sys.platform.startswith("java"):
    import platform

    os_name = platform.java_ver()[3][0]
    if os_name.startswith("Windows"):  # "Windows XP", "Windows 7", etc.
        SYSTEM_ = "win32"
    elif os_name.startswith("Mac"):  # "Mac OS X", etc.
        SYSTEM_ = "darwin"
    else:  # "Linux", "SunOS", "FreeBSD", etc.
        # Setting this to "linux2" is not ideal, but only Windows or Mac
        # are actually checked for and the rest of the module expects
        # *sys.platform* style strings.
        SYSTEM_ = "linux2"
else:
    SYSTEM_ = sys.platform

SYSTEM = SYSTEM_


class SystemEnum(enum.Enum):
    """
    Enum for the system type
    """

    windows, linux, mac, other = range(4)


def set_system(system: SystemEnum) -> None:
    """

    :param system:
    :type system:
    """
    global SYSTEM
    SYSTEM = system


def get_system() -> SystemEnum:
    """

    :return:
    :rtype:
    """
    return SYSTEM


# print(SYSTEM)
if SYSTEM == "darwin":
    SYSTEM = SystemEnum.mac
elif SYSTEM == "linux2" or SYSTEM == "linux":
    SYSTEM = SystemEnum.linux
elif SYSTEM == "win32":
    SYSTEM = SystemEnum.windows
else:
    SYSTEM = SystemEnum.other


def get_backend_module(project_name: str, backend_name: str = sys.platform) -> ModuleType:
    """Returns the backend module.

    :param project_name:
    :type project_name:
    :param backend_name:
    :type backend_name:
    :return:
    :rtype:

    """
    import importlib

    try:
        importlib.import_module(f"{project_name}")
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"{project_name} not found, please install it")

    modules = []
    if backend_name is not None:
        modules += [backend_name]
    elif sys.platform == "darwin":
        modules += ["darwin"]
    elif sys.platform == "win32":
        modules += ["win10"]
    else:
        modules += [
            "appindicator",
            "gtk",
            "xorg",
            "gtk_dbus"
            # "unity", "kde", "gnome", "fallback",
        ]

    errors = []
    for module in modules:
        try:
            return importlib.import_module(f"{project_name}.{module}")
        except ImportError as e:
            errors.append(e)

    # Did not find any backend, raise error
    raise ImportError(f'{sys.platform} platform is not supported: {"; ".join(str(e) for e in errors)}')


def is_py3():
    """

    :return:
    :rtype:
    """
    return sys.version_info[0] == 3


if __name__ == "__main__":
    print(get_backend_module("draugr", "python_utilities"))
