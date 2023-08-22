#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 23/07/2020
           """

__all__ = ["recursive_flatten"]

from typing import Sequence, Iterable


def recursive_flatten_seq(seq: Sequence) -> Sequence:
    """Depth first flatten"""
    if not seq:  # is empty Sequence
        return seq
    if isinstance(seq[0], Sequence):
        return (*recursive_flatten(seq[0]), *recursive_flatten(seq[1:]))
    return (*seq[:1], *recursive_flatten(seq[1:]))


def recursive_flatten(sequence: Iterable) -> Iterable:
    """
    Depth first flatten iterable

    >>> list(recursive_flatten([1, [2], 3]))
    [1, 2, 3]
    >>> list(recursive_flatten([1, [2], [3, [4]]]))
    [1, 2, 3, 4]
    >>> list(recursive_flatten((([[None]], 2), (2,), 2)))
    [None, 2, 2, 2]
    """
    for element in sequence:
        if isinstance(element, Iterable):
            yield from recursive_flatten(element)
        else:
            yield element


if __name__ == "__main__":
    print(list(recursive_flatten((((2,), 2), (2,), 2))))
    print(list(recursive_flatten((([[None]], 2), (2,), 2))))

    print(list(recursive_flatten((([[None]], 2), (2,), 2))))
