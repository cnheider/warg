#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 11/12/2019
           """

__all__ = ["PostInit"]

from typing import Sequence, MutableMapping


class PostInit(type):
    """
    define a new metaclass which overrides the "__call__" function"""

    def __call__(cls, *args: Sequence, **kwargs: MutableMapping):
        """
        Called when you call a class type constructor()"""
        obj = type.__call__(cls, *args, **kwargs)
        if hasattr(obj, "__post_init__"):
            obj.__post_init__(*args, **kwargs)
        return obj


if __name__ == "__main__":

    class SAD(metaclass=PostInit):
        """description"""

        def __init__(self):
            print("init")

        def __post_init__(self):
            """description"""
            print("post_init")

    SAD()
    SAD()
