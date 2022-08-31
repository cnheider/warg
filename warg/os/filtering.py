#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/30/22
           """

__all__ = []

from functools import wraps
from pathlib import Path
from typing import Callable, Sequence, MutableMapping


def is_python_module(path: Path) -> bool:
    """
    Check if path is a python module
    """
    return path.is_file() and path.suffix == ".py"


def is_python_package(path: Path) -> bool:
    """
    Check if path is a python package
    """
    return path.is_dir() and (path / "__init__.py").exists()


def negate(f: Callable) -> Callable:
    """
    Negate a function return
    """

    @wraps(f)
    def wrapper(*args: Sequence, **kwargs: MutableMapping):
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        return not f(*args, **kwargs)

    return wrapper
