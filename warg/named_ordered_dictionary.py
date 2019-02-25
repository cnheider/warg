#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Mapping
from functools import partial, wraps
from typing import Any, Iterable
import time
import sorcery

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

  #__slots__ = ('_unnamed_arg_i','__dict__')

  #_unnamed_arg_i = 0

  def __init__(self, *args: Any, **kwargs: Any):
    # super().__init__(**kwargs)

    if len(args) == 1 and type(args[0]) is dict:
      args_dict = args[0]
    else:
      args_dict = {}
      if len(args) == 1 and isinstance(args[0], Iterable):
        args = args[0]
      for arg in args:
        args_dict[f'arg{id(arg)}'] = arg

    args_dict.update(kwargs)
    self.update(args_dict or {})

  def list(self):
    return self.as_list()

  def as_list(self):
    return list(self.__dict__.values())

  def dict(self):
    return self.as_dict()

  def as_dict(self):
    return self.__dict__

  def tuple(self):
    return self.as_tuple()

  def as_tuple(self):
    return tuple(self.as_list())

  def add_unnamed_arg(self, arg):
    self.__dict__[f'arg{id(arg)}'] = arg

  @sorcery.spell
  def dict_of(frame_info, *args, **kwargs):
    """
    Instead of:

        {'foo': foo, 'bar': bar, 'spam': thing()}

    or:

        dict(foo=foo, bar=bar, spam=thing())

    write:

        dict_of(foo, bar, spam=thing())

    In other words, returns a dictionary with an item for each argument,
    where positional arguments use their names as keys,
    and keyword arguments do the same as in the usual dict constructor.

    The positional arguments can be any of:

      - plain variables,
      - attributes, or
      - subscripts (square bracket access) with string literal keys

    So the following:

        dict_of(spam, x.foo, y['bar'])

    is equivalent to:

        dict(spam=spam, foo=x.foo, bar=y['bar'])

    *args are not allowed.

    To give your own functions the ability to turn positional argments into
    keyword arguments, use the decorator magic_kwargs.

    """

    result = sorcery.dict_of.at(frame_info)(*args, **kwargs)
    return NamedOrderedDictionary(result)

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

  def __add__(self, other):
    if isinstance(other, NamedOrderedDictionary):
      for k in other.keys():
        if k in self.__dict__:
          self.__dict__[k] += other.__dict__[k]
        else:
          self.__dict__[k] = other.__dict__[k]
    elif isinstance(other, Iterable):
      for arg in other:
        self.add_unnamed_arg(arg)
    else:
      self.add_unnamed_arg(other)
    return self.__dict__


NOD = NamedOrderedDictionary

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

  vals = [1, 3, 5]
  nodict = NamedOrderedDictionary(10, val2=2, *vals)
  nolist = nodict.as_list()
  assert nolist[0] == 10
  assert nodict.val2 == 2
  assert nolist[-2] == vals[-1]

  nodict = NamedOrderedDictionary('str_parameter', 10)
  odict = {**nodict}
  assert nodict.as_list()[0] == list(odict.values())[0]

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

  columns = NamedOrderedDictionary.dict_of(arg1, aræa=arg0)
  assert columns['arg1'] == arg1
  assert columns['aræa'] == arg0

  a = NamedOrderedDictionary(4,2)
  b = a+a
  assert a.list()== [8,4]

