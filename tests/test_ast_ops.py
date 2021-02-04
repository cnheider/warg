#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 28-01-2021
           """

from warg import get_first_arg_name, identity


def test_ausdh3():
    from typing import Any

    def some_func(a: Any) -> None:
        print(get_first_arg_name("some_func", verbose=True))

    some_func(print(2, sep="-"))


def test_ausd2h3():
    from typing import Any

    def some_func(a: Any) -> None:
        print(get_first_arg_name("some_func", verbose=True))

    some_func(identity(2))


def test_ausd2h3213():
    from typing import Any

    class Ac:
        class Bc:
            @staticmethod
            def c(d):
                pass

    def some_func(a: Any) -> None:
        print(get_first_arg_name("some_func", verbose=True))

    some_func(Ac.Bc.c(2))


if __name__ == "__main__":
    test_ausdh3()
    test_ausd2h3()
    test_ausd2h3213()
