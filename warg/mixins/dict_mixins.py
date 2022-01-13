#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = [
    "IterDictItemsMixin",
    "IterDictKeysMixin",
    "IterDictValuesMixin",
]


class IterDictItemsMixin:
    """
    Mixin class for iterating kw pairs in a class instance __dict__"""

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class IterDictKeysMixin:
    """
    Mixin class for iterating only the keys of a class instance __dict__"""

    def __iter__(self):
        for attr in self.__dict__.keys():
            yield attr


class IterDictValuesMixin:
    """
    Mixin class for iterating only the values of a class instance __dict__"""

    def __iter__(self):
        for value in self.__dict__.values():
            yield value


if __name__ == "__main__":

    def asdij() -> None:
        """
        :rtype: None
        """

        class IASD(IterDictValuesMixin):
            pass

        a = IASD()
        a.b = 1
        a.c = 2
        a.d = 3

        for ca in a:
            print(ca)

    asd()
    asdij()
