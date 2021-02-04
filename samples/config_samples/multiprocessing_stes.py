#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15-12-2020
           """

from multiprocessing import Pool


def f(x):
    import config1

    print(config1.A_CONSTANT)
    return x * x


if __name__ == "__main__":
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
