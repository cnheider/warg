#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/11/2019
           """

__all__ = ["pre_decorate", "post_decorate"]

from typing import Callable


def pre_decorate(method: Callable, *callables: Callable) -> callable:
    def pre_call_func(self: object = None, *args, **kwargs) -> callable:
        for c in callables:
            c(self, *args, **kwargs)
        return method(self, *args, **kwargs)

    return pre_call_func


def post_decorate(method: Callable, *callables: Callable) -> callable:
    def post_call_func(self: object = None, *args, **kwargs) -> callable:
        res = method(self, *args, **kwargs)
        for c in callables:
            c(self, *args, res=res, **kwargs)
        return res

    return post_call_func


if __name__ == "__main__":

    def juahsdu() -> None:
        def c(d):
            print(d)
            return f"c_{d}"

        a = pre_decorate(c, lambda *args, **kwargs: print(f"pre {args, kwargs}"))
        b = post_decorate(c, lambda *args, **kwargs: print(f"post {args, kwargs}"))

        print(a("yo"))
        print(b("bro"))

    juahsdu()
