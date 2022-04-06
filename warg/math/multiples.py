#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 13-01-2021
           """

__all__ = ["lcm"]

try:
    from math import lcm
except:
    from math import gcd
    from warg import Number

    def lcm(a: Number, b: Number) -> Number:
        """Least common multiple"""
        return abs(a * b) / gcd(a, b) if a and b else 0
