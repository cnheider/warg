#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Any,
    ItemsView,
    Iterable,
    KeysView,
    List,
    MutableMapping,
    Sized,
    Tuple,
    Type,
    TypeVar,
    ValuesView,
)

import sorcery
from sorcery.core import node_name

__author__ = "Christian Heider Nielsen"

__all__ = ["NamedOrderedDictionary", "NOD"]

LOCALS = (
    "as_list",
    "as_dict",
    "as_tuples",
    "as_flat_tuples",
    "add_unnamed_arg",
    "dict_of",
    "keys",
    "update",
    "__setattr__",
)


class IllegalAttributeKey(Exception):
    """
  An exception for when a deemed illegal attribute key was being overwritten
  """

    def __init__(self, key, type_: Type):
        Exception.__init__(
            self, f'Overwriting of attribute "{key}" on type "{type_.__name__}" is not allowed'
        )


T = TypeVar("T", bound="NamedOrderedDictionary")


class NamedOrderedDictionary(MutableMapping):
    """

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
nodict.update({'paramA': 20, 'paramB': 'other_param', 'paramC': 5.0})
assert nodict.paramA == 20
assert nodict.paramB == 'other_param'

.. code-block:: python

nodict = NamedOrderedDictionary('str_parameter', 10)
nodict.update({'arg1': 20, 'arg0': 'other_param'})
assert nodict.arg0 == 'other_param'
assert nodict.arg1 == 20

.. code-block:: python

nodict = NamedOrderedDictionary(paramA='str_parameter', paramB=10)
nodict.update(20,'other_param')
assert nodict.paramB == 'other_param'
assert nodict.paramA == 20

"""

    # __slots__ = ('_unnamed_arg_i','__dict__')

    # _unnamed_arg_i = 0

    def __init__(self, *args, **kwargs) -> None:
        # super().__init__(**kwargs)
        if len(args) == 1 and isinstance(args[0], dict):
            args_dict = args[0]
        else:
            args_dict = {}
            if len(args) == 1 and isinstance(args[0], Iterable):
                args = args[0]
            for arg in args:
                args_dict[id(arg)] = arg

        args_dict.update(kwargs)
        self.update(args_dict or {})

    def as_list(self) -> list:
        """

    :return:
    :rtype:
    """
        return list(self.__dict__.values())

    def as_dict(self) -> dict:
        """

    :return:
    :rtype:
    """
        return self.__dict__

    def as_tuples(self) -> List[Tuple[Any, Any]]:
        """

    :return:
    :rtype:
    """
        return [(k, v) for (k, v) in self.__dict__.items()]

    def as_flat_tuples(self) -> List[Tuple]:
        """

    :return:
    :rtype:
    """
        return [(k, *v) for (k, v) in self.__dict__.items()]

    def add_unnamed_arg(self, arg: Any) -> None:
        """

    :param arg:
    :type arg:
    """
        self.__dict__[f"arg{id(arg)}"] = arg

    @staticmethod
    @sorcery.spell
    def nod_of(frame_info, *args, **kwargs) -> T:
        """Instead of:

{'foo': foo, 'bar': bar, 'spam': thing()}

or:

dict(foo=foo, bar=bar, spam=thing())

write:

NOD.dict_of(foo, bar, spam=thing())

In other words, returns a NamedOrderedDictionary with an item for each argument,
where positional arguments use their names as keys,
and keyword arguments do the same as in the usual dict constructor.

The positional arguments can be any of:

- plain variables,
- attributes, or
- subscripts (square bracket access) with string literal keys

So the following:

NOD.dict_of(spam, x.foo, y['bar'])

is equivalent to:

NOD.dict_of(spam=spam, foo=x.foo, bar=y['bar'])

*args are not allowed.

:rtype: object

"""
        nod = NamedOrderedDictionary()

        for arg, value in zip(frame_info.call.args[-len(args) :], args):
            try:
                arg_key = node_name(arg)
                nod[arg_key] = value
            except TypeError:
                nod.add_unnamed_arg(value)

        nod.update(kwargs)

        return nod

    def __getattr__(self, item: Any) -> Any:
        if item == "__deepcopy__":
            return super().__getattribute__(item)
        return self.__dict__[item]

    def __len__(self) -> int:
        return len(self.__dict__)

    def __setattr__(self, key: Any, value: Any) -> None:
        if key in LOCALS:
            raise IllegalAttributeKey(key, type_=NamedOrderedDictionary)

        if key == "__dict__":
            super().__setattr__(key, value)
        else:
            self.__dict__[key] = value

    def __getitem__(self, key: Any) -> Any:
        """
    NOTE getting a tuple is a unique key

    :param key:
    :type key:
    :return:
    :rtype:
    """
        if isinstance(key, slice):
            keys = list(self.__dict__.keys())[key]
            return [self.__dict__[a] for a in keys]
        elif isinstance(key, KeysView):
            # assert set(self.__dict__.keys()).issuperset(key)
            return [self.__dict__[a] for a in key]
        return self.__dict__[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
    NOTE setting a tuple is a unique key

    :param key:
    :type key:
    :param value:
    :type value:
    """
        if isinstance(key, slice):
            keys = list(self.__dict__.keys())[key]
            if isinstance(value, Sized):
                assert len(keys) == len(
                    value
                ), f"number of keys {len(keys)} are not equal values {len(value)}"
                for a, v in zip(keys, value):
                    self.__dict__[a] = v
            else:
                for a in keys:
                    self.__dict__[a] = value
        elif isinstance(key, KeysView):
            # assert set(self.__dict__.keys()).issuperset(key)
            # assert isinstance(value,Sized), f'values must be of type Sized, was {type(value)},' \
            #                                f' distribution is not supported'
            if isinstance(value, Sized):
                assert len(key) == len(value), f"number of keys {len(key)} are not equal values {len(value)}"
                for a, v in zip(key, value):
                    self.__dict__[a] = v
            else:
                for a in key:
                    self.__dict__[a] = value
        else:
            self.__dict__[key] = value

    def __delitem__(self, key) -> None:
        del self.__dict__[key]

    def keys(self) -> KeysView:
        """

    :return:
    :rtype:
    """
        return self.__dict__.keys()

    def items(self) -> ItemsView:
        """

    :return:
    :rtype:
    """
        return self.__dict__.items()

    def values(self) -> ValuesView:
        """

    :return:
    :rtype:
    """
        return self.__dict__.values()

    def __contains__(self, item) -> bool:
        return item in self.__dict__

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def __repr__(self):
        items = self.items()
        print_str = f"{self.__class__.__name__}("
        if len(items) > 0:
            for key, value in items:
                print_str += f"'{key}': {value}, "
            print_str = print_str[:-2]
        print_str += ")"
        return print_str

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
Merge two attributes, overriding any repeated keys from
the `items` parameter.

Args:
items (dict): Python dictionary containing updated values.
"""

        if len(args) == 1 and isinstance(args[0], dict):
            args_dict = args[0]
        else:
            args_dict = {}
            a = list(self.__dict__.keys())
            for arg, key in zip(args, a):
                args_dict[key] = arg

        args_dict.update(kwargs)

        for key in args_dict:
            if key in LOCALS:
                raise IllegalAttributeKey(key, type_=NamedOrderedDictionary)

        self.__dict__.update(args_dict)

    def __add__(self, other) -> T:
        cop = self.__dict__.copy()
        if isinstance(other, NamedOrderedDictionary):
            for k in other.keys():
                if k in cop:
                    cop[k] += other.__dict__[k]
                else:
                    cop[k] = other.__dict__[k]
        elif isinstance(other, Iterable):
            for arg in other:
                self.add_unnamed_arg(arg)
        else:
            self.add_unnamed_arg(other)
        return NOD(cop)

    def __sub__(self, other) -> T:
        cop = self.__dict__.copy()
        if isinstance(other, NamedOrderedDictionary):

            for k in other.keys():
                if k in cop:
                    cop[k] -= other.__dict__[k]
            return NOD(cop)
        else:
            raise ArithmeticError(f"Can not subtract {type(other)} from {type(self)}")

    def __truediv__(self, other) -> Any:
        if isinstance(other, (str, int)):
            return self.get(other)
        else:
            raise ArithmeticError(f"Can not access with {type(other)} in {type(self)}")

    def __matmul__(self, other):
        if isinstance(other, (str, int)):
            return self.get(other)
        else:
            raise ArithmeticError(f"Can not access with {type(other)} in {type(self)}")

    def __floordiv__(self, other) -> Any:
        return self.__truediv__(other)

    def __setstate__(self, state) -> None:
        self.__dict__ = state

    def __getstate__(self) -> dict:
        return self.__dict__

    def __call__(self, *args) -> List:
        return [self.get(a) for a in args]


NOD = NamedOrderedDictionary

if __name__ == "__main__":

    nodict = NamedOrderedDictionary()
    nodict.paramA = "str_parameter"
    nodict.paramB = 10
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    from copy import deepcopy, copy

    b = copy(nodict)
    print(b)
    assert b.paramB == 10
    assert b.paramB == nodict.paramB

    a = deepcopy(nodict)
    print(a)
    assert a.paramB == 10
    assert a.paramB == nodict.paramB
