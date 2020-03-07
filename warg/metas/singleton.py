#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

__all__ = ["SingletonBase", "SingletonMeta"]


class SingletonBase:
    """
A base class for creating singleton class where all subtypes(Deriavations) should also return the first
and only
instantiation of a particular singleton base type, if this property is not wanted consider using the
SingletonMeta class instead.
"""

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance


class SingletonMeta(type):
    """
Conversely the SingletonBase, this base meta class is used for creating singleton class where all
subtypes(
Deriavations) should only
return
singleton instantiations of a particular singleton type independantly of subtyping and super-types,
if this property is not
wanted
consider using
the
SingletonBase class instead.
"""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance


if __name__ == "__main__":

    class SingletonBaseClass(SingletonBase):
        pass

    class S1(SingletonBaseClass):
        pass

    class SingletonBaseMeta(metaclass=SingletonMeta):
        pass

    class S2(SingletonBaseMeta):
        pass

    print(SingletonBaseClass())
    print(SingletonBaseClass())
    print(S1())

    print(SingletonBaseMeta())
    print(SingletonBaseMeta())
    print(S2())
