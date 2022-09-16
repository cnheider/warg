#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/5/22
           """

__all__ = ["export"]

import sys


# @export # Sadly can not be used here as it not declared yet :/ ;)
def export(fn):
    """

    A decorator that exports function in the containing modules all in not already existent.

    works but code analysis tools usually complains

        :param fn:
        :type fn:
        :return:
        :rtype:
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, "__all__"):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn
