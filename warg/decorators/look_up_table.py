#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          Automatically generates a look up data

           Created on 06/03/2020
           """

from time import sleep, time
from typing import Iterable, Set, Mapping, Tuple

from warg.decorators.hashing import make_hash

global_table = {}

__all__ = ["add_lut", "look_up", "look_up_args", "look_up_kws"]


def add_lut(f: callable):
    global_table[f] = {}
    return f


def look_up(f, *args, **kwargs):
    ag_hash = hash(args) + make_hash(kwargs)
    if f in global_table:
        if ag_hash in global_table[f]:
            return global_table[f][ag_hash]

        res = global_table[f][ag_hash] = f(*args, **kwargs)
        return res

    global_table[f] = {}
    res = global_table[f][ag_hash] = f(*args, **kwargs)
    return res


def look_up_args(f, *args):
    if f in global_table:
        if args in global_table[f]:
            return global_table[f][args]

        res = global_table[f][args] = f(*args)
        return res

    global_table[f] = {}
    res = global_table[f][args] = f(*args)
    return res


def look_up_kws(f, **kws):
    kw_hash = make_hash(kws)
    if f in global_table:
        if kw_hash in global_table[f]:

            return global_table[f][kw_hash]

        res = global_table[f][kw_hash] = f(**kws)
        return res

    global_table[f] = {}
    res = global_table[f][kw_hash] = f(**kws)
    return res


def precompute_lut(f: callable, arg_sets: Set[Tuple[Iterable, Mapping]], *, verbose=False) -> callable:
    for arg_set, kws_set in arg_sets:
        res = look_up(f, *arg_set, **kws_set)
        if verbose:
            print(f"precompute {f},{arg_set},{kws_set}->{res}")
    return f


def precompute_lut_args(f: callable, arg_sets: Set[Iterable], *, verbose=False) -> callable:
    for arg_set in arg_sets:
        res = look_up_args(f, *arg_set)
        if verbose:
            print(f"precompute {f},{arg_sets}->{res}")
    return f


def precompute_lut_kws(f: callable, arg_sets: Set[Mapping], *, verbose=False) -> callable:
    for arg_set in arg_sets:
        res = look_up_kws(f, **arg_set)
        if verbose:
            print(f"precompute {f},{arg_sets}->{res}")
    return f


def precompute_lut_dec(arg_sets, *, verbose=False):
    def rdec(f):
        precompute_lut(f, arg_sets, verbose=verbose)
        return f

    return rdec


def precompute_lut_args_dec(arg_sets, *, verbose: bool = False):
    def rdec(f):
        precompute_lut_args(f, arg_sets, verbose=verbose)
        return f

    return rdec


if __name__ == "__main__":

    @add_lut
    def my_function(foo, bar):
        return foo + bar

    result = look_up_args(my_function, 0, 8)
    print(result)
    result = look_up_args(my_function, 8, 0)
    print(result)

    @precompute_lut_args_dec(list(zip(range(9), reversed(range(9)))))
    def my_function2(foo, bar):
        sleep(0.1)
        return bar * foo

    a = time()
    look_up_args(my_function2, 0, 8)
    print(time() - a)
    a = time()
    look_up_args(my_function2, 8, 0)
    print(time() - a)

    result = look_up(my_function2, 14, bar=21)
    print(result)

    result = look_up(my_function2, 14, bar=21)
    print(result)

    result = look_up(my_function2, 104, bar=2)
    print(result)

    result = look_up_args(my_function, 1, 2)
    print(result)

    result = look_up_args(my_function, 1, 2)
    print(result)

    result = look_up_args(my_function, 12, 2)
    print(result)

    result = look_up_args(my_function2, 1, 2)
    print(result)

    result = look_up_kws(my_function2, foo=1, bar=2)
    print(result)