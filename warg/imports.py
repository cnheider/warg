#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 28/06/2020
           """

from importlib.util import find_spec


def is_module_available(module: str) -> bool:
    """**Return True if module is available.**

  Parameters
  ----------
  module: str
          Name of the module to be checked.

  Returns
  -------
  bool
          True if installed.

  """
    return find_spec(module) is not None
