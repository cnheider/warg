#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Iterable, Iterator, Mapping, Tuple, Sized

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 11/11/2019
           """

__all__ = ["yield_and_map", "inner_map", "kw_map"]


def yield_and_map(iterable: Iterable, level: int = 0, func: callable = print) -> Any:
    """

    :param iterable:
    :type iterable:
    :param level:
    :type level:
    :param func:
    :type func:"""
    if level == 0:
        for a in iterable:
            func(a)
            yield a
    elif level == 1:
        for a in iterable:
            for b in a:
                func(b)
                yield b
    elif level == 2:
        for a in iterable:
            for b in a:
                for c in b:
                    func(c)
                    yield c


def inner_map(func: callable, iterable: Iterable, aggregate_yield: bool = True) -> Any:
    """

    :param func:
    :type func:
    :param iterable:
    :type iterable:
    :param aggregate_yield:
    :type aggregate_yield:"""
    if aggregate_yield:
        for a in iterable:
            yield [func(b) for b in a]
    else:
        for a in iterable:
            for b in a:
                yield func(b)


def kw_map(func: callable, kw: str, iterable: Iterable) -> Any:
    """

    :param func:
    :type func:
    :param kw:
    :type kw:
    :param iterable:
    :type iterable:"""
    for a in iterable:
        yield func(**{kw: a})


def select_key(tuple_iterator: Iterable, *a) -> Tuple:
    """
    Yield keys from mapping if in a

    :param tuple_iterator:
    :type tuple_iterator:
    :param a:
    :type a:
    :return:
    :rtype:
    """
    for k, _ in tuple_iterator:
        if k in a:
            yield k, _


def select_dict(mapping: Mapping, *a) -> Mapping:
    """
    Select keys from mapping if in a

    Args:
      mapping:
      *a:

    Returns:

    """
    return {k: v for k, v in select_key(mapping.items(), *a)}


if __name__ == "__main__":

    def uahsd():
        agfas = (2, 3)
        # TODO

        sadd = {a: b for a, b in zip("abcdef", range(6))}
        print(select_dict(sadd, "a", "d"))

    uahsd()
