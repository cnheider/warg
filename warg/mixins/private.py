#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/9/22
           """

__all__ = ["PrivateAttributeMixin"]

from typing import Any


class PrivateAttributeMixin:
    def __getitem__(self, key: str) -> Any:
        if key.startswith("_"):
            return None
        return getattr(self, key, None)
