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
        self.args_a = args
        self.kwargs_a = kwargs

    def something(self):
        print(self.kwargs_a)

    def something_else(self, *args):
        print(args, self.kwargs_a)

    def another(self, *args, **kwargs):
        print(args, self.kwargs_a, kwargs)

    def clearly_something(self, *args, **kwargs):
        print(self.args_a, args, self.kwargs_a, kwargs)


def test_not_both():
    try:
        GeneralisedDelayedKwargConstruction(A, [1], a=2)
    except Exception as e:
        assert isinstance(e, AssertionError)


def test_kw():
    GeneralisedDelayedKwargConstruction(A, a=2)


def test_mapping():
    da = GeneralisedDelayedKwargConstruction(A, {"a": 2})
    a = da(99)
    a.something()
    a.clearly_something(231, b="52")


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
