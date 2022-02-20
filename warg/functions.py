#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/01/2020
           """

__all__ = [
    "kws_sink",
    "sink",
    "prod",
    "collate_first_dim",
    "call_identity",
    "args_sink",
    "identity",
    "invert_shallow_mapping",
    "flip_two_level_mapping",
    "swap_mapping_order",
    "nop",
]

import operator
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from typing import Any, Callable, Dict, Iterable, Iterator, Mapping, Sequence, Tuple

from warg import Number, drop_unused_kws


def nop() -> None:
    """
    :rtype: None
    """
    pass


def identity(a: Any) -> Any:
    """ """
    return a


@drop_unused_kws
def kws_sink(*args) -> Tuple[Any, ...]:
    """
    Returns args without any modification what so ever. Drops kws
    :return:"""
    return args


def call_identity(*args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    """

    :param args:
    :param kwargs:
    :return:"""
    return args, kwargs


# noinspection PyUnusedLocal
def args_sink(*args, **kwargs) -> Dict[str, Any]:
    """

    :param args:
    :param kwargs:
    :return:"""
    return kwargs


# noinspection PyUnusedLocal
def sink(*args, **kwargs) -> None:
    """
    Returns None, but accepts everything

    :param args:
    :param kwargs:
    :return:"""
    return None


def prod(iterable: Iterable[Number]) -> Number:
    """
    Calculate the product of the a Iterable of int or floats
    :param iterable:
    :return:"""
    return reduce(operator.mul, iterable, 1)


def collate_first_dim(batch: Iterable) -> Tuple:
    """

    :param batch:
    :return:"""
    return tuple(zip(*batch))


def invert_shallow_mapping(m: Mapping) -> Dict:
    """

    :param m:
    :return:
    """
    return {v: k for k, v in m.items()}


def flip_two_level_mapping(m: Mapping) -> Dict:
    """
    result = {}
    [result.setdefault(a, {}).update({k:b}) for k, v in m.items() for a, b in v.items()]
    return result

    :param m:
    :return:
    """

    flipped = defaultdict(dict)
    for key, val in m.items():
        for sub_key, sub_val in val.items():
            flipped[sub_key][key] = sub_val
    return flipped


def swap_mapping_order(m: Mapping, order: Sequence[int]) -> Mapping:
    """

    :param m:
    :param order:
    :return:
    """
    order = [*order]

    def deep_swap(dict_, level):
        """

        :param dict_:
        :param level:
        :return:
        """

        def swap_two_level_dict(a):
            """

            :param a:
            :return:
            """
            b = defaultdict(dict)
            for key1, value1 in a.items():
                for key2, value2 in value1.items():
                    b[key2].update({key1: value2})
            return b

        dict_ = deepcopy(dict_)
        if level == 0:
            dict_ = swap_two_level_dict(dict_)
        else:
            for key in dict_:
                dict_[key] = deep_swap(dict_[key], level - 1)
        return dict_

    for pas_no in range(len(order) - 1, 0, -1):
        for i in range(pas_no):
            if order[i] > order[i + 1]:
                temp = order[i]
                order[i] = order[i + 1]
                order[i + 1] = temp
                m = deep_swap(m, i)
    return m


def chain_filter(it: Iterable, *filters: Callable) -> Iterator:
    """
    Apply a sequence of callables to an iterable through filter; filtering the iterable to the subset of a callable
    returns

    Args:
        it (Iterable):
            iterable to be filtered
        filters (Callable):
            The filter callables

    Returns:
        Iterator:
            returns an iterator yielding those items of iterable for which all(filters(item)) is true. If filters are
            None, return the items that are true.
    """
    for f in filters:
        it = filter(f, it)
    return it


def chain_apply(it: Iterable, *callables: Callable) -> Iterable:
    """
    Apply a sequence of callables to an iterable; apply the iterable sequentially in callables order

    Args:
        it (Iterable):
            iterable to be applied to
        callables (Callable):
             The applying callables

    Returns:
        Iterable:
            returns the iterable with all the callables applied.
    """
    for f in callables:
        it = f(it)
    return it


if __name__ == "__main__":

    def asud() -> None:
        """
        :rtype: None
        """
        a = {"b": 1, "h": 2}
        print(invert_shallow_mapping(a))

    def asjdnasid() -> None:
        """
        :rtype: None
        """
        a = {
            "b": {"c": {"d": [0, 1, 2], "e": [3, 4, 5, 6]}, "f": [7, 8], "g": [9]},
            "h": {"j": [10, 11]},
        }
        print(flip_two_level_mapping(a))

    def asidj() -> None:
        """
        :rtype: None
        """
        test_dict = {
            "a": {"c": {"e": 0, "f": 1}, "d": {"e": 2, "f": 3}},
            "b": {"c": {"g": 4, "h": 5}, "d": {"j": 6, "k": 7}},
        }
        result = swap_mapping_order(test_dict, [2, 0, 1])
        print(result)

    # asud()
    asidj()
    # asjdnasid()
