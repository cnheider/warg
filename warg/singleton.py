#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""


class SingletonBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance


class SingletonMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance


class SingletonBaseClass(SingletonBase):
    pass


class S1(SingletonBaseClass):
    pass


class SingletonBaseMeta(metaclass=SingletonMeta):
    pass


class S2(SingletonBaseMeta):
    pass


if __name__ == "__main__":
    print(SingletonBaseClass())
    print(SingletonBaseClass())
    print(S1())

    print(SingletonBaseMeta())
    print(SingletonBaseMeta())
    print(S2())
