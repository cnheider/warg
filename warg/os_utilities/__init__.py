#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = r"""

           Created on 17/02/2020
           """

__author__ = "Christian Heider Nielsen"

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()
# del Path

from .os_platform import *
from .path_utilities import *
from .filtering import *
from .platform_selection import *
from .path_functions import *
