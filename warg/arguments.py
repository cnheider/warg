#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from collections import namedtuple
from pathlib import Path, PosixPath
from typing import Mapping, Tuple
from warnings import warn

import wrapt

from warg.named_ordered_dictionary import NOD

__author__ = "Christian Heider Nielsen"

__all__ = [
    "to_lower_properties",
    "get_upper_case_vars_or_protected_of",
    "config_to_mapping",
    "add_bool_arg",
    "check_for_duplicates_in_args",
    "wrap_args",
    "UpperAttrMetaclass",
]


class UpperAttrMetaclass(type):
    """
    Upper case all attributes if not __private
    """

    def __new__(cls, clsname, bases, dct: dict):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith("__"):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)


class ConfigObject(object):
    """
    Config object
    """

    pass


def to_lower_properties(C_dict: Mapping):
    """

    :param C_dict:
    :type C_dict:
    :return:
    :rtype:
    """
    if not isinstance(C_dict, dict):
        C_dict = config_to_mapping(C_dict)

    a = ConfigObject()

    for (k, v) in C_dict.items():
        assert isinstance(k, str)
        lowered = k.lower()
        if isinstance(v, (PosixPath, Path)):
            setattr(a, lowered, str(v))
        else:
            setattr(a, lowered, v)

    return a


def lower_dict(map: Mapping) -> Mapping:
    """

    :param map:
    :type map:
    :return:
    :rtype:
    """
    cop = {}
    for (k, v) in map.items():
        assert isinstance(k, str)
        cop[k.lower()] = v

    return cop


def upper_dict(map: Mapping) -> Mapping:
    """

    :param map:
    :type map:
    :return:
    :rtype:
    """
    cop = {}
    for (k, v) in map.items():
        assert isinstance(k, str)
        cop[k.upper()] = v

    return cop


def get_upper_case_vars_or_protected_of(module: object, lower_keys: bool = True) -> Mapping:
    """

    :param module:
    :type module:
    :param lower_keys:
    :type lower_keys:
    :return:
    :rtype:
    """
    v = vars(module)
    check_for_duplicates_in_args(**v)
    if v:
        if lower_keys:
            return {
                key.lower(): value
                for key, value in module.__dict__.items()
                if (key.isupper() or (key.startswith("_")) and not key.endswith("_"))
            }
        return {
            key: value
            for key, value in module.__dict__.items()
            if (key.isupper() or (key.startswith("_")) and not key.endswith("_"))
        }
    return {}


def config_to_mapping(C: object, only_upper_case: bool = True) -> NOD:
    """

    :param C:
    :type C:
    :param only_upper_case:
    :type only_upper_case:
    :return:
    :rtype:
    """
    if only_upper_case:
        return NOD(get_upper_case_vars_or_protected_of(C))
    else:
        return NOD(vars(C))


def add_bool_arg(
    parser: argparse.ArgumentParser,
    name: str,
    *,
    dest: str = None,
    converse: str = None,
    default: bool = False,
    **kwargs,
):
    """

    :param parser:
    :type parser:
    :param name:
    :type name:
    :param dest:
    :type dest:
    :param converse:
    :type converse:
    :param default:
    :type default:
    :param kwargs:
    :type kwargs:
    """
    if not dest:
        dest = name

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument(f"--{name.upper()}", f"-{name.lower()}", dest=dest, action="store_true", **kwargs)
    if converse:
        group.add_argument(
            f"--{converse.upper()}", f"-{converse.lower()}", dest=dest, action="store_false", **kwargs
        )
    else:
        group.add_argument(
            f"--NO-{name.upper()}", f"-no-{name.lower()}", dest=dest, action="store_false", **kwargs
        )
    parser.set_defaults(**{dest: default})


def check_for_duplicates_in_args(**kwargs) -> None:
    """

    :param kwargs:
    :type kwargs:
    """
    for key, value in kwargs.items():

        occur = 0

        if kwargs.get(key) is not None:
            occur += 1
        else:
            pass

        if key.isupper():
            k_lowered = f"_{key.lower()}"
            if kwargs.get(k_lowered) is not None:
                occur += 1
            else:
                pass
        else:
            k_lowered = f'{key.lstrip("_").upper()}'
            if kwargs.get(k_lowered) is not None:
                occur += 1
            else:
                pass

        if occur > 1:
            warn(f"Config contains hiding duplicates of {key} and {k_lowered}, {occur} times")


def wrap_args(n_tuple: namedtuple):
    """

    :param n_tuple:
    :type n_tuple:
    :return:
    :rtype:
    """

    @wrapt.decorator(adapter=n_tuple)
    def wrapper(wrapped, instance, args, kwargs):
        """

        :param wrapped:
        :type wrapped:
        :param instance:
        :type instance:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        if isinstance(args[0], n_tuple):
            n = args[0]
        else:
            n = n_tuple(*args, **kwargs)
        return wrapped(n)

    return wrapper


def str_to_bool(s: str, preds: Tuple[str, ...] = ("true", "1")) -> bool:
    """


:param s:
:return:
"""
    return s.lower() in preds


str2bool = str_to_bool

if __name__ == "__main__":

    c = namedtuple("C", ("a", "b"))

    @wrap_args(c)
    def add(v):
        """

        :param v:
        :type v:
        :return:
        :rtype:
        """
        return v.a + v.b

    def add2(a, b):
        """

        :param a:
        :type a:
        :param b:
        :type b:
        :return:
        :rtype:
        """
        return a + b

    h = add(2, 2)
    print(h)

    j = add(c(1, 4))
    print(j)

    wq = add2(2, 4)
    print(wq)

    wc = add2(*c(4, 3))
    print(wc)
