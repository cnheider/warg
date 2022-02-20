#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import sys

__all__ = ["is_nix", "is_windows"]

CUR_OS = sys.platform
IS_WIN = any(CUR_OS.startswith(i) for i in ["win32", "cygwin"])
IS_NIX = any(CUR_OS.startswith(i) for i in ["aix", "linux", "darwin"])


def is_windows() -> bool:
    """

    :return:
    """
    return IS_WIN


def is_nix() -> bool:
    """

    :return:
    """
    return IS_NIX
