#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy

__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = ["IterItemsMixin", "IterKeysMixin", "IterDictValuesMixin", "IndexDictTuplesMixin"]


class IterItemsMixin(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class IterKeysMixin(object):
    def __iter__(self):
        for attr in self.__dict__.keys():
            yield attr


class IterDictValuesMixin(object):
    def __iter__(self):
        for value in self.__dict__.values():
            yield value


class IndexDictTuplesMixin(object):
    def __getitem__(self, item):
        if isinstance(item, int):
            a = self.__dict__
            b = numpy.array(list(a.values()))
            return b[item]
        else:
            return self.__dict__[item]


if __name__ == "__main__":

    def asd():
        class IDTM(IndexDictTuplesMixin):
            pass

        a = IDTM()
        a.a = 2
        a.b = 3
        assert a[0] == 2

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
