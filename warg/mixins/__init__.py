#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = r"""

           Created on 17/02/2020
           """

__author__ = "Christian Heider Nielsen"

import pathlib

with open(pathlib.Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()

from .dict_mixins import *
