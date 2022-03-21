#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          This file is not for general use. Ode to python

           Created on 13/06/2020
           """

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
