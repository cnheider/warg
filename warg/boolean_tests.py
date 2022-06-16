#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02/01/2020
           """

__all__ = [
    "is_positive_and_mod_zero",
    "is_zero_or_mod_zero",
    "is_none_or_zero_or_negative",
    "is_zero_or_mod_below",
    "is_none_or_zero_or_negative_or_mod_zero",
    "xor",
    "xnor",
    "nand",
]

import math
from typing import Any, Optional

from warg import Number
from warg.decorators import drop_unused_kws, passes_kws_to


@drop_unused_kws
def is_positive_and_mod_zero(
    mod: Optional[Number],
    counter: int,
    *,
    ret: Any = True,
    alt: Any = False,
    residual_printer: callable = None,
) -> Any:
    """

    test if mod is positive
    then test if counter % mod is 0
    if both tests are true return ret
    else return alt


    :param residual_printer:
    :type residual_printer:
    :param mod:
    :param counter:
    :param ret:
    :param alt:
    :return:"""

    if mod == 0:
        if residual_printer is not None:
            residual_printer(math.inf)
        return alt

    m = counter % mod
    if residual_printer is not None:
        residual_printer(m)

    return ret if (mod > 0 and (m == 0)) else alt


@drop_unused_kws
def is_zero_or_mod_below(
    mod: Optional[Number],
    below: Number,
    counter: int,
    *,
    ret: Any = True,
    alt: Any = False,
    residual_printer: callable = None,
) -> Any:
    """

    test if mod is zero or if counter % mod is 0
    if any of the tests are true return ret
    else return alt


    :param residual_printer:
    :type residual_printer:
    :param below:
    :type below:
    :param mod:
    :param counter:
    :param ret:
    :param alt:
    :return:"""
    if mod == 0:
        if residual_printer is not None:
            residual_printer(0)
        return ret

    m = counter % mod
    if residual_printer is not None:
        residual_printer(m - below)

    return ret if (m < below) else alt


@drop_unused_kws
def is_zero_or_mod_zero(
    mod: Optional[Number],
    counter: int,
    *,
    ret: Any = True,
    alt: Any = False,
    residual_printer: callable = None,
) -> Any:
    """

    test if mod is zero or if counter % mod is 0
    if any of the tests are true return ret
    else return alt


    :param residual_printer:
    :type residual_printer:
    :param mod:
    :param counter:
    :param ret:
    :param alt:
    :return:"""

    if mod == 0:
        if residual_printer is not None:
            residual_printer(0)
        return ret

    m = counter % mod
    if residual_printer is not None:
        residual_printer(m)

    return ret if (m == 0) else alt


@drop_unused_kws
def is_none_or_zero_or_negative(obj: Optional[Number], residual_printer: callable = None) -> bool:
    """

    :param residual_printer:
    :type residual_printer:
    :param obj:
    :return:"""
    is_none = obj is None
    is_negative = False
    if isinstance(obj, (int, float)):
        is_negative = obj <= 0

    if is_none:
        if residual_printer is not None:
            residual_printer(0)
    else:
        if residual_printer is not None:
            residual_printer(obj)

    return is_none or is_negative


@passes_kws_to(is_zero_or_mod_zero)
def is_none_or_zero_or_negative_or_mod_zero(mod: Optional[Number], counter: int, **kwargs) -> bool:
    """

    :param mod:
    :param counter:
    :param kwargs:
    :return:"""
    return is_none_or_zero_or_negative(mod, **kwargs) or is_zero_or_mod_zero(mod, counter, **kwargs)


def xor(a: bool, b: bool) -> bool:
    """

    :param a:
    :param b:
    :return:"""
    return a ^ b


def xnor(a: bool, b: bool) -> bool:
    """

    :param a:
    :param b:
    :return:"""
    return not xor(a, b)


def nand(a: bool, b: bool) -> bool:
    """

    :param a:
    :param b:
    :return:"""
    return not (a and b)


if __name__ == "__main__":
    assert is_zero_or_mod_below(5, 3, 7) == True
    assert is_zero_or_mod_below(5, 2, 4) == False
    for i in range(9):
        print(is_zero_or_mod_zero(1, i))
    for i in range(9):
        print(is_zero_or_mod_zero(2, i))

    print()
    for i in range(8):
        print(is_none_or_zero_or_negative_or_mod_zero(None, i, residual_printer=print))

    for i in range(8):
        print(is_none_or_zero_or_negative_or_mod_zero(True, 4 - i, residual_printer=print))
