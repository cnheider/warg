#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/11/2019
           """

__all__ = ["timeit"]

import time
from functools import wraps


def timeit(f: callable):
    @wraps(f)
    def wrapper(*args, **kwds):
        start_time = time.time()
        result = f(*args, **kwds)
        elapsed_time = time.time() - start_time
        print(f"{f} took {elapsed_time:.3f} seconds to compute")
        return elapsed_time, result

    return wrapper
