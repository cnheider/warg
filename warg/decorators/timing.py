#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/11/2019
           """

__all__ = ["timeit"]

import functools
import time
from functools import wraps


def timeit(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """

        :param args:
        :type args:
        :param kwds:
        :type kwds:
        :return:
        :rtype:
        """
        start_time = time.time()
        result = f(*args, **kwds)
        elapsed_time = time.time() - start_time
        print(f"{f} took {elapsed_time:.3f} seconds to compute")
        return elapsed_time, result

    return wrapper


def singleton(cls):
    """ Use class as singleton. """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        """

        @param cls:
        @type cls:
        @param args:
        @type args:
        @param kw:
        @type kw:
        @return:
        @rtype:
        """
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls
