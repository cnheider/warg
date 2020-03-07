#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 11/12/2019
           """

__all__ = ["PostInit"]


class PostInit(type):
    """
define a new metaclass which overrides the "__call__" function
"""

    def __call__(cls, *args, **kwargs):
        """Called when you call a class type constructor() """
        obj = type.__call__(cls, *args, **kwargs)
        if hasattr(obj, "__post_init__"):
            obj.__post_init__(*args, **kwargs)
        return obj
