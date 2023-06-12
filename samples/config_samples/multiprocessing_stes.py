#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15-12-2020
           """

if __name__ == "__main__":

    def _main():
        from multiprocessing import Pool

        def f(x):
            """description"""
            import config1

            print(config1.A_CONSTANT)
            return x * x

        with Pool(5) as p:
            print(p.map(f, [1, 2, 3]))

    _main()
