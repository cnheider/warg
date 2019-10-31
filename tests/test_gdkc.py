#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from warg.gdkc import GeneralisedDelayedKwargConstruction

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
            Much like the partial wrapper from functools, GeneralisedDelayedKwargConstruction provides a 
            way of finishing constrution of class instance or call of function but lets you change the 
            kwargs until actual call.
           """


class A:
    def __init__(self, *args, **kwargs):
        pass


def test_not_both():
    GeneralisedDelayedKwargConstruction(A, [1], a=2)


def test_kw():
    GeneralisedDelayedKwargConstruction(A, a=2)


def test_mapping():
    GeneralisedDelayedKwargConstruction(A, {"a": 2})


def test_overwriting_warning(caplog):
    ssc = GeneralisedDelayedKwargConstruction(A, {"a": 2})

    ssc(a=1)

    assert "Overwriting" in caplog.text


def test_mapping_and_args_fail():
    with pytest.raises(AssertionError) as exc_info:
        GeneralisedDelayedKwargConstruction(A, {"a": 2}, 1)

    assert exc_info.type is AssertionError


def test_mapping_and_args_fail_inv():
    with pytest.raises(AssertionError) as exc_info:
        GeneralisedDelayedKwargConstruction(A, 1, {"a": 2})

    assert exc_info.type is AssertionError
