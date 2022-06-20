#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "heider"
__doc__ = r"""

           Created on 01/02/2022
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()
# del Path

from .color_conversion import *
from .css_colors import *
from .label_colors import *
