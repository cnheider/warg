#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ["IterDictItemsMixin", "IterDictKeysMixin", "IterDictValuesMixin", "OrdinalIndexingDictMixin"]


class IterDictItemsMixin:
    """
    Mixin class for iterating kw pairs in a class instance __dict__
    """

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class IterDictKeysMixin:
    """
Mixin class for iterating only the keys of a class instance __dict__
"""

    def __iter__(self):
        for attr in self.__dict__.keys():
            yield attr


class IterDictValuesMixin:
    """
Mixin class for iterating only the values of a class instance __dict__
"""

    def __iter__(self):
        for value in self.__dict__.values():
            yield value


class OrdinalIndexingDictMixin:
    """
Mixin class for indexing a class instance __dict__ (SortedDict) with both integer (ordinal) indexing or
key:str attributes (non-ordinal) access.
"""

    def __getitem__(self, item):
        if isinstance(item, int):
            a = self.__dict__
            b = numpy.array(list(a.values()))
            return b[item]
        else:
            return self.__dict__[item]


if __name__ == "__main__":

    def asd():
        class IDTM(OrdinalIndexingDictMixin):
            pass

        a = IDTM()
        a.a = 2
        a.b = 3
        assert a[0] == 2
        assert a[1] == 3

    def asdij():
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
