#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 28-01-2021
           """

from warg import kws_sink, prod, sink


def test_a():
    print((kws_sink("str")))
    print((kws_sink(2)))
    print((kws_sink(2.2)))

    print((prod((2, 2))))

    print((prod((2.2, 2.2))))

    print((prod((2, 2.2))))

    print((prod((2.2, 2))))

    print((sink((2, 2), face=(2.2, 2))))
