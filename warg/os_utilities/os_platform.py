#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          get os platform path_utilities 

           Created on 13/06/2020
           """

__all__ = ["is_nix", "is_windows", "is_mac", "is_linux", "get_platform", "has_x_server"]

CUR_OS = sys.platform
IS_WIN = any(CUR_OS.startswith(i) for i in ["win32", "cygwin"])
IS_LINUX = CUR_OS.startswith("linux")
IS_MAC = CUR_OS.startswith("darwin")
IS_NIX = IS_LINUX or IS_MAC or CUR_OS.startswith("aix")


def is_windows() -> bool:
    """

    :return:
    """
    return IS_WIN


def is_linux() -> bool:
    """

    :return:
    """
    return IS_LINUX


def is_nix() -> bool:
    """

    :return:
    """
    return IS_NIX


def is_mac() -> bool:
    """

    :return:
    """
    return IS_MAC


def get_platform() -> str:
    """

    :return:
    """
    return CUR_OS


def has_x_server() -> bool:
    """
    test if display is available, if other than linux system atm it returns true

    :return:
    :rtype:
    """
    if is_nix():
        return "DISPLAY" in os.environ and os.environ["DISPLAY"] != ""

    return True
