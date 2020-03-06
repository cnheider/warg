#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 9/14/19
           """


def test_print(capsys):
    """Correct my_name argument prints"""
    text = "hello"
    err = "world"
    print(text)
    sys.stderr.write("world")
    captured = capsys.readouterr()
    assert text in captured.out
    assert err in captured.err
