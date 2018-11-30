#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Collection, Iterable

__author__ = 'cnheider'


class NamedOrderedDict:
  '''

  Usage:

      .. code-block:: python

          nodict = NamedOrderedDict()
          nodict.paramA = 'myparam'
          nodict.paramB = 10
          assert nodict.paramA == 'myparam'
          assert nodict.paramB == 10

      .. code-block:: python

          nodict = NamedOrderedDict({'paramA': 'myparam', 'paramB': 10})
          assert nodict.paramA == 'myparam'
          assert nodict.paramB == 10

      .. code-block:: python

          nodict = NamedOrderedDict(paramA='myparam', paramB=10)
          assert nodict.paramA == 'myparam'
          assert nodict.paramB == 10

      .. code-block:: python

          nodict = NamedOrderedDict('myparam', 10)
          assert nodict.arg0 == 'myparam'
          assert nodict.arg1 == 10

      .. code-block:: python

          arg0,arg1 = NamedOrderedDict('myparam', 10).as_list()
          assert arg0 == 'myparam'
          assert arg1 == 10

      As with dictionaries you can use the `update()` method.

      .. code-block:: python
          nodict = NamedOrderedDict()
          nodict.update({'paramA': 20, 'paramB': 'otherparam', 'paramC': 5.0})
          assert nodict.paramA == 20
          assert nodict.paramB == 'otherparam'

      .. code-block:: python

          nodict = NamedOrderedDict('myparam', 10)
          nodict.update({'arg1': 20, 'arg0': 'otherparam'})
          assert nodict.arg0 == 'otherparam'
          assert nodict.arg1 == 20

      .. code-block:: python

          nodict = NamedOrderedDict(paramA='myparam', paramB=10)
          nodict.update(20,'otherparam')
          assert nodict.paramB == 'otherparam'
          assert nodict.paramA == 20

  '''

  def __init__(self, *args: Any, **kwargs: Any):
    if len(args) == 1 and type(args[0]) is dict:
      args_dict = args[0]
    else:
      i = 0
      args_dict = {}
      if len(args) == 1 and isinstance(args[0], Iterable):
        args = args[0]
      for arg in args:
        args_dict[f'arg{i}'] = arg
        i += 1

    args_dict.update(kwargs)
    self.update(args_dict or {})

  def as_list(self):
    return list(self.__dict__.values())

  def __getattr__(self, item):
    return self.__dict__[item]

  def __setattr__(self, key, value):
    self.__dict__[key] = value

  def __iter__(self):
    for key, value in self.__dict__.items():
      yield key, value

  def __repr__(self):
    print_str = ''
    for key, value in self:
      print_str += f'{key}: {value}\n'
    return print_str

  def update(self, *args: Any, **kwargs: Any) -> None:
    '''
    Merge two attributes, overriding any repeated keys from
    the `items` parameter.

    Args:
        items (dict): Python dictionary containing updated values.
    '''

    if len(args) == 1 and type(args[0]) is dict:
      args_dict = args[0]
    else:
      args_dict = {}
      a = list(self.__dict__.keys())
      for arg, key in zip(args, a):
        args_dict[key] = arg

    args_dict.update(kwargs)

    self.__dict__.update(args_dict)


if __name__ == '__main__':

  nodict = NamedOrderedDict()
  nodict.paramA = 'myparam'
  nodict.paramB = 10
  assert nodict.paramA == 'myparam'
  assert nodict.paramB == 10

  nodict = NamedOrderedDict({'paramA':'myparam', 'paramB':10})
  assert nodict.paramA == 'myparam'
  assert nodict.paramB == 10

  nodict = NamedOrderedDict()
  nodict.update({'paramA':20, 'paramB':'otherparam', 'paramC':5.0})
  nodict.paramA = 10
  assert nodict.paramA == 10
  assert nodict.paramB == 'otherparam'

  nodict = NamedOrderedDict('myparam', 10)
  nodict.update(arg1=20, arg0='otherparam')
  assert nodict.arg0 == 'otherparam'
  assert nodict.arg1 == 20

  nodict = NamedOrderedDict('myparam', 10)
  nodict.update({'arg1':20, 'arg0':'otherparam'})
  assert nodict.arg0 == 'otherparam'
  assert nodict.arg1 == 20

  nodict = NamedOrderedDict(paramA='myparam', paramB=10)
  nodict.update(20, 'otherparam')
  assert nodict.paramB == 'otherparam'
  assert nodict.paramA == 20

  arg0, arg1 = NamedOrderedDict('myparam', 10).as_list()
  assert arg0 == 'myparam'
  assert arg1 == 10

  print('success')
