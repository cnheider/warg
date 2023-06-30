#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/30/22
           """

__all__ = ["is_excluded", "is_python_package", "is_python_module", "negate"]

import re
from functools import wraps
from pathlib import Path
from typing import Callable, Sequence, MutableMapping, Union, Any


def is_python_module(path: Path) -> bool:
    """
    Check if path is a python module
    """
    path = Path(path)

    return path.is_file() and path.suffix == ".py"


def is_python_package(path: Path) -> bool:
    """
    Check if path is a python package
    """
    path = Path(path)
    return path.is_dir() and (path / "__init__.py").exists()


def is_excluded(path: Union[Path, str], exclude_pattern: str = "[Ee]xcluded*"):
    """
    is exclude by common pattern or gitignore

    #TODO: Look up nearest parent git ignore and interpret

    :param exclude_pattern:
    :type exclude_pattern:
    :param path:
    :type path:
    :return:
    :rtype:
    """

    if len(re.findall(exclude_pattern, str(path))) > 0:
        return True
    return False


def negate(f: Callable) -> Callable:
    """
    Negate a function return
    """

    assert isinstance(f, Callable), "ensure you did not call the callable with parameters directly"

    @wraps(f)
    def wrapper(*args: Sequence[Any], **kwargs: MutableMapping[str, Any]) -> Any:
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


if __name__ == "__main__":
    # print(negate(is_excluded("/iods/excludes/osad.py")))
    print(negate(is_excluded)("/iods/excludes/osad.py"))
    print(is_excluded("/s/excludes/a.py"))
    print(is_excluded("/s/exclud/a.py"))
    print(is_excluded("/s/exclude/a.py"))
    print(is_excluded("/s/Exclude/a.py"))
    print(is_excluded("/s/excluded/a.py"))
    print(is_excluded("/s/Excluded/a.py"))
