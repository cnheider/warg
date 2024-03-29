#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 09/03/2020
           """

from warg import kws_sink, prod, sink, evaluate_context


def test_a():
    print(evaluate_context(kws_sink, "str"))
    print(evaluate_context(kws_sink, 2))
    print(evaluate_context(kws_sink, 2.2))

    print(evaluate_context(prod, (2, 2)))

    print(evaluate_context(prod, (2.2, 2.2)))

    print(evaluate_context(prod, (2, 2.2)))

    print(evaluate_context(prod, (2.2, 2)))

    print(evaluate_context(sink, (2, 2), face=(2.2, 2)))
