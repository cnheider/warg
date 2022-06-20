#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = ""

__all__ = [
    "OrdinalIndexingDictMixin",
]


class OrdinalIndexingDictMixin:
    """
    Mixin class for indexing a class instance __dict__ (SortedDict) with both integer (ordinal) indexing or
    key:str attributes (non-ordinal) access."""

    def __getitem__(self, item):
        if isinstance(item, int):
            return list(self.__dict__.values())[item]
        else:
            return self.__dict__[item]


if __name__ == "__main__":

    def asd() -> None:
        """
        :rtype: None
        """

        class IDTM(OrdinalIndexingDictMixin):
            pass

        a = IDTM()
        a.a = 2
        a.b = 3
        assert a[0] == 2
        assert a[1] == 3
