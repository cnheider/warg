#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 21/12/2019
           """

from collections import defaultdict


def AutoDict():
    """

    :return:
    :rtype:
    """
    return defaultdict(autodict)


def recursive_default_dict_print(d, depth=1):
    """

    :param d:
    :type d:
    :param depth:
    :type depth:
    """
    for k, v in d.items():
        print("-" * depth, k)
        if type(v) is defaultdict:
            recursive_default_dict_print(v, depth + 1)
        else:
            print("-" * (depth + 1), v)


def sanitise_auto_dict(d):
    """

    :param d:
    :type d:
    :return:
    :rtype:
    """
    if isinstance(d, defaultdict):
        if len(d.keys()) == 0:
            return None

    out_dict = dict()
    for k, v in d.items():
        if isinstance(v, defaultdict):
            sanitised = sanitise_auto_dict(v)
            if sanitised is None:
                continue
            out_dict[k] = sanitised
        else:
            out_dict[k] = v
    if len(out_dict) > 0:
        return out_dict
    return None


autodict = AutoDict
AD = AutoDict

if __name__ == "__main__":
    ad = AutoDict()

    a = ad["b"]["b"]["b"]["b"]
    ad["b"]["b"]["c"]["b"]["c"] = {}
    ad["c"] = 1
    ad["cd"]["v"] = 1
    ad["qc"]["d"] = []
    ad["cf"]["b6"] = None
    ad["cf"]["1"] = None

    print(ad)

    recursive_default_dict_print(ad)

    print(sanitise_auto_dict(ad))
