#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"

import time


def benchmark_func(func, times=100000):
    start = time.time()
    result = None
    for _ in range(times):
        result = func()
    end = time.time()
    return end - start, result
