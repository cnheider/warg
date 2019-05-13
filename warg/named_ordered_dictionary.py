#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Mapping
from typing import Any, Iterable

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
        msg = f'Overwritting of attribute "{key}" on type "{type}" is not allowed'
        Exception.__init__(self, msg)


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
    def dict_of(frame_info, *args, **kwargs):
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

    def __getitem__(self, item) -> Any:
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
        print_str = f"{self.__class__.__name__}("
        for key, value in self:
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

    def __sub__(self, other):
        if isinstance(other, NamedOrderedDictionary):
            for k in other.keys():
                if k in self.__dict__:
                    self.__dict__[k] -= other.__dict__[k]
        else:
            raise ArithmeticError(f"Can not subtract {type(other)} from {type(self)}")

    def __truediv__(self, other):
        if isinstance(other, str):
            return self.get(other)
        else:
            raise ArithmeticError(f"Can not access with {type(other)} in {type(self)}")

    def __floordiv__(self, other):
        return self.__truediv__(other)


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
    assert nodict.as_list()[0] == list(odict.values())[0]

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

    columns = NamedOrderedDictionary.dict_of(arg1, aræa=arg0)
    assert columns["arg1"] == arg1
    assert columns.arg1 == arg1
    assert columns["aræa"] == arg0
    assert columns / "aræa" == arg0
    assert id(columns / "aræa") == id(columns["aræa"])

    a = NamedOrderedDictionary(4, 2)
    a.list = "a"
    assert a.list == "a"

    a = NamedOrderedDictionary(4, 2)
    b = a + a
    assert a.as_list() == [8, 4]
