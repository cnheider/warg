#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Any, MutableMapping

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ["GeneralisedDelayedKwargConstruction", "GDKC"]


class GeneralisedDelayedKwargConstruction(object):
    """
A generalised class for setting up kwargs for later construction of an instance of an object
"""

    def __init__(self, constructor: callable, *args, **kwargs):
        """

:param constructor:
:param args:
:param kwargs:
"""
        self.constructor: callable = constructor
        assert len(args) < 2
        assert not (len(kwargs) > 1 and len(args) > 1)

        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], MutableMapping):
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
