#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15-12-2020
           """

if __name__ == "__main__":

    def f():
        import config1

        print(config1.A_CONSTANT)
        import config1

        print(config1.ANOTHER_CONSTANT)

    f()
