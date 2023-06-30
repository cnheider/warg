#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence, MutableMapping, Any

from warg import drop_unused_kws
from warg.metas.post_init import PostInit

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
           """


def test_post_init_class():
    class MyTestingClass(metaclass=PostInit):
        """
        class with the metaclass passed as an argument"""

        @drop_unused_kws
        def __init__(self, *args: Sequence[Any], **kwargs: MutableMapping[str, Any]):
            print(kwargs)

        def __post_init__(self, *args: Sequence[Any], **kwargs: MutableMapping[str, Any]):
            print(args, kwargs)

        def __call__(self, *args: Sequence[Any], **kwargs: MutableMapping[str, Any]):
            print("a")

    a = MyTestingClass("asdc", kas=2)

    a()


def test_post_init_no_kws_class():
    class MyTestingClass(metaclass=PostInit):
        """
        class with the metaclass passed as an argument"""

        @drop_unused_kws
        def __init__(self, *args: Sequence):
            print("Init class")

        @drop_unused_kws
        def __post_init__(self, *args: Sequence):
            print(args)

        def __call__(self, *args: Sequence[Any], **kwargs: MutableMapping[str, Any]):
            print("a")

    a = MyTestingClass("asdc", kas=2)

    a()


def test_no_post_init_class():
    class MyTestingClass(metaclass=PostInit):
        """
        class with the metaclass passed as an argument"""

        def __init__(self):
            print("Init class")

        def __call__(self, *args: Sequence[Any], **kwargs: MutableMapping[str, Any]):
            print("a")

    a = MyTestingClass()

    a()
