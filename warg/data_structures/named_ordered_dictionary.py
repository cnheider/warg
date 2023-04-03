#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Any,
    ItemsView,
    Iterable,
    KeysView,
    List,
    MutableMapping,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    ValuesView,
    Mapping,
)

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

RECURSE_MAPPING_CONVERSION = True


def recurse_conversion(self, value):
    if isinstance(value, MutableMapping) and not isinstance(value, self.__class__):
        value = self.__class__(value)
    elif isinstance(value, (list, tuple)):  # TODO: MAYBE KEEP?
        value = type(value)(
            self.__class__(x) if isinstance(x, MutableMapping) else recurse_conversion(self, x) for x in value
        )
    return value


class IllegalAttributeKey(Exception):
    """
    An exception for when a deemed illegal attribute key was being overwritten"""

    def __init__(self, key: Any, type_: Type):
        Exception.__init__(
            self,
            f'Overwriting of attribute "{key}" on type "{type_.__name__}" is not allowed',
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
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
        if len(args_dict) > 0:
            self.update(args_dict)

    def as_list(self) -> list:
        """

        :return:
        :rtype:"""
        return list(self.__dict__.values())

    def as_dict(self) -> dict:
        """

        :return:
        :rtype:"""
        return self.__dict__

    def as_tuples(self) -> List[Tuple[Any, Any]]:
        """

        :return:
        :rtype:"""
        return [(k, v) for (k, v) in self.__dict__.items()]

    def as_flat_tuples(self) -> List[Tuple]:
        """

        :return:
        :rtype:"""
        return [(k, *v) for (k, v) in self.__dict__.items()]

    def add_unnamed_arg(self, arg: Any) -> None:
        """

        :param arg:
        :type arg:"""
        self.__dict__[f"arg{id(arg)}"] = arg

    '''
import sorcery
from sorcery.core import node_name

@staticmethod
@sorcery.spell  # TODO: MAY BE BROKEN!
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
'''

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
            if RECURSE_MAPPING_CONVERSION:
                value = recurse_conversion(self, value)
            self.__dict__[key] = value

    def __getitem__(self, key: Any) -> Any:
        """
        NOTE getting a tuple is a unique key

        :param key:
        :type key:
        :return:
        :rtype:"""
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
        :type value:"""
        if isinstance(key, slice):
            keys = list(self.__dict__.keys())[key]
            if isinstance(value, Sequence):
                assert len(keys) == len(
                    value
                ), f"number of keys {len(keys)} are not equal values {len(value)}"
                for a, v in zip(keys, value):
                    if RECURSE_MAPPING_CONVERSION:
                        v = recurse_conversion(self, v)
                    self.__dict__[a] = v
            else:
                for a in keys:
                    if RECURSE_MAPPING_CONVERSION:
                        value = recurse_conversion(self, value)
                    self.__dict__[a] = value
        elif isinstance(key, KeysView):
            # assert set(self.__dict__.keys()).issuperset(key)
            # assert isinstance(value,Sequence), f'values must be of type Sequence, was {type(value)},' \
            #                                f' distribution is not supported'
            if isinstance(value, (Sequence, ValuesView)):
                assert len(key) == len(value), f"number of keys {len(key)} are not equal values {len(value)}"
                for a, v in zip(key, value):
                    if RECURSE_MAPPING_CONVERSION:
                        v = recurse_conversion(self, v)
                    self.__dict__[a] = v
            else:
                for a in key:
                    if RECURSE_MAPPING_CONVERSION:
                        value = recurse_conversion(self, value)
                    self.__dict__[a] = value
        else:
            if RECURSE_MAPPING_CONVERSION:
                value = recurse_conversion(self, value)
            self.__dict__[key] = value

    def __delitem__(self, key) -> None:
        del self.__dict__[key]

    def keys(self) -> KeysView:
        """

        :return:
        :rtype:"""
        return self.__dict__.keys()

    def items(self) -> ItemsView:
        """

        :return:
        :rtype:"""
        return self.__dict__.items()

    def values(self) -> ValuesView:
        """

        :return:
        :rtype:"""
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

    def update(self, *args: Any, **kwargs: Any) -> T:
        """
        Merge two attributes, overriding any repeated keys from
        the `items` parameter.

        :returns self

        Args:
        items (dict): Python dictionary containing updated values."""

        if len(args) == 1 and isinstance(args[0], Mapping):
            a: Mapping = args[0]
            if RECURSE_MAPPING_CONVERSION and True:
                l = {}
                for k, v in a.items():
                    l[k] = recurse_conversion(self, v)
                a = l

            args_dict = a
        elif len(args):
            args_dict = {}
            a: List = list(self.__dict__.keys())
            if True:  # be same length guard
                assert len(a) == len(args)
            for arg, key in zip(args, a):
                if RECURSE_MAPPING_CONVERSION and True:
                    arg = recurse_conversion(self, arg)

                args_dict[key] = arg
        else:
            args_dict = {}
            # print('no args where supplied')

        args_dict.update(kwargs)

        for key in args_dict:
            if key in LOCALS:
                raise IllegalAttributeKey(key, type_=NamedOrderedDictionary)

        self.__dict__.update(args_dict)
        return self

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

    def __call__(self, *args: Sequence) -> List:
        return [self.get(a) for a in args]


NOD = NamedOrderedDictionary

if __name__ == "__main__":
    from itertools import count

    ccc = count()

    print(f"\n{next(ccc):#^9}")  # 0
    nodict = NamedOrderedDictionary()
    nodict.paramA = "str_parameter"
    nodict.paramB = 10
    print(nodict)
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    from copy import deepcopy, copy

    print(f"\n{next(ccc):#^9}")  # 1
    b = copy(nodict)
    print(b)
    assert b.paramB == 10
    assert b.paramB == nodict.paramB

    print(f"\n{next(ccc):#^9}")  # 2
    a = deepcopy(nodict)
    print(a)
    assert a.paramB == 10
    assert a.paramB == nodict.paramB

    print(f"\n{next(ccc):#^9}")  # 3
    c = NOD()
    c[nodict.keys()] = nodict.values()
    print(c)
    d = deepcopy(c)
    print(d)

    print(f"\n{next(ccc):#^9}")  # 4
    nodict = NamedOrderedDictionary()
    nodict.paramA = {"s": "str_parameter"}
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.s)

    print(f"\n{next(ccc):#^9}")  # 5
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA["s"] = "str_parameter"
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.s)

    print(f"\n{next(ccc):#^9}")  # 6
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA.s = "str_parameter"
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.s)

    print(f"\n{next(ccc):#^9}")  # 7
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA["s"] = [{"sd": "str_parameter"}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.s)

    print(f"\n{next(ccc):#^9}")  # 8
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA.s = [{"sd": "str_parameter"}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.s)

    print(f"\n{next(ccc):#^9}")  # 9
    nodict = NamedOrderedDictionary()
    nodict.paramA = [{"s": {"sd": "str_parameter"}}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 10
    nodict = NamedOrderedDictionary()
    nodict.paramA = [{"s": ({"sd": "str_parameter"},)}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 11
    nodict = NamedOrderedDictionary()
    nodict.paramA = [{"sd": "str_parameter"}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 12
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA.a = [{"s": {"sd": "str_parameter"}}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 13
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA.a = [{"s": ({"sd": "str_parameter"},)}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA.a)

    print(f"\n{next(ccc):#^9}")  # 14
    nodict = NamedOrderedDictionary()
    nodict.paramA = {}
    nodict.paramA.a = [{"s": [{"sd": "str_parameter"}]}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 15
    nodict = NamedOrderedDictionary()
    nodict.paramA = [{"s": {"sd": "str_parameter"}}, {"sfd": 1}]
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)

    print(f"\n{next(ccc):#^9}")  # 16
    nodict = NamedOrderedDictionary()
    nodict.paramA = {"s": {"sd": {"sfd": 1}}}
    nodict.paramB = 10
    # assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10
    print(nodict)
    print(nodict.paramA)
