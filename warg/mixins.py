#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy

__author__ = "Christian Heider Nielsen"
__doc__ = ""


__all__ = ["IterItemsMixin", "IterKeysMixin", "IterValuesMixin", "IndexDictTuplesMixin"]


class IterItemsMixin(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class IterKeysMixin(object):
    def __iter__(self):
        for attr in self.__dict__.keys():
            yield attr


class IterValuesMixin(object):
    def __iter__(self):
        a = self.__dict__
        for value in a.values():
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
