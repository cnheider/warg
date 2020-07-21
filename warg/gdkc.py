#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Any, Mapping, MutableMapping

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ["GeneralisedDelayedKwargConstruction", "GDKC"]


class GeneralisedDelayedKwargConstruction(object):
    """
A generalised class for setting up kwargs for later construction of an instance of an object
[constructor, args, kwargs]

"""

    def __init__(self, constructor: callable, *args, **kwargs):
        """
[constructor, args, kwargs]
:param constructor:
:param args:
:param kwargs:
"""
        self.constructor: callable = constructor
        assert len(args) < 2, f"Does not support multiple args, only a single mapping type"
        if len(args) == 1:
            assert isinstance(
                args[0], Mapping
            ), f"Arg[0] type is not a mapping type, was {type(args[0])} which is not supported"
        assert not (
            len(kwargs) > 0 and len(args) > 0
        ), f"Does not support both args and kwargs, both supplied args, {args} and {kwargs}"

        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], Mapping):
            self.kwargs: MutableMapping = args[0]
        elif len(kwargs) == 1 and next(iter(kwargs.keys())) == "kwargs":
            self.kwargs = kwargs["kwargs"]
        else:
            self.kwargs: MutableMapping = kwargs

    def __call__(self, *args, **kwargs) -> Any:
        """

:param args:
:param kwargs:
:return:
"""

        war = "".join(
            [
                f"Overwriting {k} with the value {v} in construction of {self.constructor}"
                for (k, v), b in zip(kwargs.items(), self.kwargs.keys())
                if k == b
            ]
        )
        if war != "":
            logging.warning(war)

        self.kwargs.update(kwargs)
        try:
            return self.constructor(*args, **self.kwargs)
        except TypeError as e:
            e.args += (f"in construction of {self.constructor}",)
            raise e


GDKC = GeneralisedDelayedKwargConstruction

if __name__ == "__main__":

    class A:
        def __init__(self, *args, **kwargs):
            pass

    def test_not_both():
        GeneralisedDelayedKwargConstruction(A, [1], a=2)

    def test_kw():
        GeneralisedDelayedKwargConstruction(A, a=2)

    def test_mapping():
        GeneralisedDelayedKwargConstruction(A, {"a": 2})

    def test_mapping_and_args_fail():
        GeneralisedDelayedKwargConstruction(A, {"a": 2}, 1)

    def test_mapping_and_args_fail_inv():
        GeneralisedDelayedKwargConstruction(A, 1, {"a": 2})

    test_kw()
    test_mapping()
    try:
        test_mapping_and_args_fail()
        raise Exception
    except:
        pass
    try:
        test_mapping_and_args_fail_inv()
        raise Exception
    except:
        pass
    test_not_both()
