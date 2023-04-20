#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 26-01-2021
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()
# del Path

from .arg_indentifier import *
from .first_arg_identifier import *
