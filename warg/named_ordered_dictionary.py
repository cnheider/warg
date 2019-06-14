#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Mapping
from typing import Any, Iterable, Sized, TypeVar, KeysView

import sorcery

__author__ = "cnheider"

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
    def __init__(self, key, type):
        msg = f'Overwriting of attribute "{key}" on type "{type}" is not allowed'
        Exception.__init__(self, msg)


T = TypeVar("T", bound="NamedOrderedDictionary")


class NamedOrderedDictionary(Mapping):
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # super().__init__(**kwargs)

        if len(args) == 1 and isinstance(args[0], dict):
            args_dict = args[0]
        else:
            args_dict = {}
            if len(args) == 1 and isinstance(args[0], Iterable):
                args = args[0]
            for arg in args:
                args_dict[f"arg{id(arg)}"] = arg

        args_dict.update(kwargs)
        self.update(args_dict or {})

    def as_list(self):
        return list(self.__dict__.values())

    def as_dict(self):
        return self.__dict__

    def as_tuples(self):
        return [(k, v) for (k, v) in self.__dict__.items()]

    def as_flat_tuples(self):
        return [(k, *v) for (k, v) in self.__dict__.items()]

    def add_unnamed_arg(self, arg):
        self.__dict__[f"arg{id(arg)}"] = arg

    @sorcery.spell
    def nod_of(frame_info, *args, **kwargs) -> T:
        """
Instead of:

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

        result = sorcery.dict_of.at(frame_info)(*args, **kwargs)
        return NamedOrderedDictionary(result)

    def __getattr__(self, item):
        return self.__dict__[item]

    def __len__(self):
        return len(self.__dict__)

    def __setattr__(self, key, value):
        if key in LOCALS:
            raise IllegalAttributeKey(key, type=NamedOrderedDictionary.__name__)

        self.__dict__[key] = value

    def __getitem__(self, key) -> Any:
        if isinstance(key, slice):
            keys = list(self.__dict__.keys())[key]
            return [self.__dict__[a] for a in keys]
        elif isinstance(key, KeysView):
            # assert set(self.__dict__.keys()).issuperset(key)
            return [self.__dict__[a] for a in key]
        return self.__dict__[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            keys = list(self.__dict__.keys())[key]
            for a, v in zip(keys, value):
                self.__dict__[a] = v
        elif isinstance(key, KeysView):
            # assert set(self.__dict__.keys()).issuperset(key)
            assert len(key) == len(value)
            for a, v in zip(key, value):
                self.__dict__[a] = v
        else:
            self.__dict__[key] = value

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def __contains__(self, item):
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
                raise IllegalAttributeKey(key, type=NamedOrderedDictionary.__name__)

        self.__dict__.update(args_dict)

    def __add__(self, other):
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

    def __sub__(self, other):
        cop = self.__dict__.copy()
        if isinstance(other, NamedOrderedDictionary):

            for k in other.keys():
                if k in cop:
                    cop[k] -= other.__dict__[k]
            return NOD(cop)
        else:
            raise ArithmeticError(f"Can not subtract {type(other)} from {type(self)}")

    def __truediv__(self, other):
        if isinstance(other, str):
            return self.get(other)
        else:
            raise ArithmeticError(f"Can not access with {type(other)} in {type(self)}")

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__


NOD = NamedOrderedDictionary

if __name__ == "__main__":

    nodict = NamedOrderedDictionary()
    nodict.paramA = "str_parameter"
    nodict.paramB = 10
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10

    nodict = NamedOrderedDictionary({"paramA": "str_parameter", "paramB": 10})
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10

    nodict = NamedOrderedDictionary()
    nodict.update({"paramA": 20, "paramB": "other_param", "paramC": 5.0})
    nodict.paramA = 10
    assert nodict.paramA == 10
    assert nodict.paramB == "other_param"

    nodict = NamedOrderedDictionary()
    nodict["paramA"] = 10
    assert nodict.paramA == 10

    values = [1, 3, 5]
    nodict = NamedOrderedDictionary(10, val2=2, *values)
    nolist = nodict.as_list()
    assert nolist[0] == 10
    assert nodict.val2 == 2
    assert nolist[-2] == values[-1]

    nodict = NamedOrderedDictionary("str_parameter", 10)
    odict = {**nodict}
    assert nodict.as_list()[0] == list(odict.values())[0], (nodict.as_list()[0], list(odict.values())[0])

    nodict = NamedOrderedDictionary("str_parameter", 10)
    nodict.update(arg1=20, arg0="other_param")
    assert nodict.arg0 == "other_param"
    assert nodict.arg1 == 20

    nodict = NamedOrderedDictionary("str_parameter", 10)
    nodict.update({"arg1": 20, "arg0": "other_param"})
    assert nodict.arg0 == "other_param"
    assert nodict.arg1 == 20

    nodict = NamedOrderedDictionary(paramA="str_parameter", paramB=10)
    nodict.update(20, "other_param")
    assert nodict.paramB == "other_param"
    assert nodict.paramA == 20
    assert nodict.get("paramC") is None

    nodict = NamedOrderedDictionary(paramC="str_parameter", **nodict)
    assert nodict.paramB == "other_param"
    assert nodict.paramA == 20
    assert nodict.get("paramC") is not None

    arg0, arg1 = NamedOrderedDictionary("str_parameter", 10).as_list()
    assert arg0 == "str_parameter"
    assert arg1 == 10

    columns = NamedOrderedDictionary.nod_of(arg1, aræa=arg0)
    assert columns["arg1"] == arg1
    assert columns.arg1 == arg1
    assert columns["aræa"] == arg0
    assert columns / "aræa" == arg0
    assert id(columns / "aræa") == id(columns["aræa"])

    LATEST_GPU_STATS = NamedOrderedDictionary(4, 2)
    LATEST_GPU_STATS.list = "a"
    assert LATEST_GPU_STATS.list == "a"

    LATEST_GPU_STATS = NamedOrderedDictionary(4, 2)
    b = LATEST_GPU_STATS + LATEST_GPU_STATS
    assert b.as_list() == [8, 4], b

    columns = NamedOrderedDictionary.nod_of(arg1, aræa=arg0)

    assert columns[columns.as_dict().keys()] == [arg1, arg0], columns[columns.as_dict().keys()]

    try:
        columns[columns.as_dict().keys()] = [arg1]
    except Exception as e:
        assert isinstance(e, AssertionError)

    try:
        assert columns["as", "ad"] == [arg1, arg0]
        assert False
    except Exception as e:
        assert isinstance(e, KeyError)

    columns["as", "ad"] = [arg1, arg0, 2]
    assert columns["as", "ad"] == [arg1, arg0, 2]

    assert id(columns / "aræa") == id(columns["aræa"])
