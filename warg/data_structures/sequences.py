#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          Plugin

           Created on 13/06/2020
           """

from typing import Sequence, Tuple

__all__ = ["split"]


def split(seq: Sequence) -> Tuple[Sequence, Sequence]:
    """

    :param seq:
    :type seq:
    :return:
    :rtype:
    """
    m = len(seq) // 2
    return seq[:m], seq[m:]


if __name__ == "__main__":
    print((split(list(range(11)))))
    print((split(list(range(10)))))
    print((split(list(range(9)))))
