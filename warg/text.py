#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"

__doc__ = """description"""
__all__ = ["to_british_english", "deamericanise"]

from types import MappingProxyType
from typing import Mapping

default_rules = MappingProxyType(
    {
        "ize": "ise",
        "yze": "yse",
        "iza": "isa",
        "aluminum": "aluminium"
        # 'se': 'ce',
        # 'og': 'ogue',
    }
)


def to_british_english(text: str, rules: Mapping = default_rules) -> str:
    """

    :param text:
    :type text:
    :param rules:
    :type rules:
    :return:
    :rtype:
    """
    for r in rules.items():
        text = text.replace(*r)
    return text


def deamericanise(text: str) -> str:
    """
    Naively exchanges 'z' in english texts

    convert to 'British English'

    :return:
    :rtype:
    """
    return to_british_english(text)


if __name__ == "__main__":
    print(
        deamericanise(
            "I analyzed websites in order to recognize the correct spelling of international organizations"
        )
    )
