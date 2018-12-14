#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Mapping
from functools import partial, wraps
from typing import Any, Iterable

from sorcery import dict_of

__author__ = 'cnheider'


class NamedOrderedDictionary(Mapping):
  '''

  Usage:

      .. code-block:: python

          nodict = NamedOrderedDictionary()
          nodict.paramA = 'str_parameter'
          nodict.paramB = 10
          assert nodict.paramA == 'str_parameter'
          assert nodict.paramB == 10


      .. code-block:: python

          nodict = NamedOrderedDictionary()
          nodict['paramA'] = 10
          assert nodict.paramA == 10

      .. code-block:: python

          nodict = NamedOrderedDictionary({'paramA': 'str_parameter', 'paramB': 10})
          assert nodict.paramA == 'str_parameter'
          assert nodict.paramB == 10

      .. code-block:: python

          nodict = NamedOrderedDictionary(paramA='str_parameter', paramB=10)
          assert nodict.paramA == 'str_parameter'
          assert nodict.paramB == 10

      .. code-block:: python

          nodict = NamedOrderedDictionary('str_parameter', 10)
          assert nodict.arg0 == 'str_parameter'
          assert nodict.arg1 == 10

      .. code-block:: python

          arg0,arg1 = NamedOrderedDictionary('str_parameter', 10).as_list()
          assert arg0 == 'str_parameter'
          assert arg1 == 10

      As with dictionaries you can use the `update()` method.

      .. code-block:: python
          nodict = NamedOrderedDictionary()
          nodict.update({'paramA': 20, 'paramB': 'otherparam', 'paramC': 5.0})
          assert nodict.paramA == 20
          assert nodict.paramB == 'otherparam'

      .. code-block:: python

          nodict = NamedOrderedDictionary('str_parameter', 10)
          nodict.update({'arg1': 20, 'arg0': 'otherparam'})
          assert nodict.arg0 == 'otherparam'
          assert nodict.arg1 == 20

      .. code-block:: python

          nodict = NamedOrderedDictionary(paramA='str_parameter', paramB=10)
          nodict.update(20,'otherparam')
          assert nodict.paramB == 'otherparam'
          assert nodict.paramA == 20

  '''

  def __init__(self, *args: Any, **kwargs: Any):
    # super().__init__(**kwargs)
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

  def as_dict(self):
    return self.__dict__

  def as_tuple(self):
    return tuple(self.as_list())

  def __getattr__(self, item):
    return self.__dict__[item]

  def __len__(self):
    return len(self.__dict__)

  def __setattr__(self, key, value):
    self.__dict__[key] = value

  def __getitem__(self, item):
    return self.__dict__[item]

  def __setitem__(self, key, value):
    self.__dict__[key] = value

  def keys(self):
    return self.__dict__.keys()

  def __contains__(self, item):
    return item in self.__dict__

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

  nodict = NamedOrderedDictionary()
  nodict.paramA = 'str_parameter'
  nodict.paramB = 10
  assert nodict.paramA == 'str_parameter'
  assert nodict.paramB == 10

  nodict = NamedOrderedDictionary({'paramA':'str_parameter', 'paramB':10})
  assert nodict.paramA == 'str_parameter'
  assert nodict.paramB == 10

  nodict = NamedOrderedDictionary()
  nodict.update({'paramA':20, 'paramB':'otherparam', 'paramC':5.0})
  nodict.paramA = 10
  assert nodict.paramA == 10
  assert nodict.paramB == 'otherparam'

  nodict = NamedOrderedDictionary()
  nodict['paramA'] = 10
  assert nodict.paramA == 10

  vals = (1, 3, 5)
  nodict = NamedOrderedDictionary(10, val2=2, *vals)
  assert nodict['arg0'] == 10
  assert nodict.val2 == 2
  assert (nodict.arg1, nodict.arg2, nodict.arg3) == vals
  print(f'Success! Lnodict: {nodict.as_tuple()}')

  nodict = NamedOrderedDictionary('str_parameter', 10)
  odict = {**nodict}
  print(odict)
  assert nodict.arg1 == odict['arg1']

  nodict = NamedOrderedDictionary('str_parameter', 10)
  nodict.update(arg1=20, arg0='otherparam')
  assert nodict.arg0 == 'otherparam'
  assert nodict.arg1 == 20

  nodict = NamedOrderedDictionary('str_parameter', 10)
  nodict.update({'arg1':20, 'arg0':'otherparam'})
  assert nodict.arg0 == 'otherparam'
  assert nodict.arg1 == 20

  nodict = NamedOrderedDictionary(paramA='str_parameter', paramB=10)
  nodict.update(20, 'otherparam')
  print(nodict)
  assert nodict.paramB == 'otherparam'
  assert nodict.paramA == 20
  assert nodict.get('paramC') == None

  nodict = NamedOrderedDictionary(paramC='str_parameter', **nodict)
  assert nodict.paramB == 'otherparam'
  assert nodict.paramA == 20
  assert nodict.get('paramC') != None

  arg0, arg1 = NamedOrderedDictionary('str_parameter', 10).as_list()
  assert arg0 == 'str_parameter'
  assert arg1 == 10

  columns = dict_of(arg1, aræa=arg0)
  assert columns['arg1'] == arg1
  assert columns['aræa'] == arg0
  print(columns)



  print(f'Success! Last is nodict: {nodict.as_tuple()}')
