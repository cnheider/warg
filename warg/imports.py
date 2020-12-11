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

def reimport_check():
  from sys import modules
  try:
    module = modules[module_name]
  except KeyError:
    __import__('m')

def reimport_check2():
  import importlib
  spam_spec = importlib.util.find_spec("spam")
  found = spam_spec is not None


def reimport_check3():
  import sys

  modulename = 'datetime'
  if modulename not in sys.modules:
    print(f'You have not imported the {modulename} module')

if __name__ == '__main__':
    def main():
      pass


    main()