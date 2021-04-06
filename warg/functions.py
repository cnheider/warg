#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/01/2020
           """

__all__ = [
    "kws_sink",
    "sink",
    "prod",
    "collate_first_dim",
    "call_identity",
    "args_sink",
    "identity",
    ]

import operator
from functools import reduce
from typing import Any, Dict, Iterable, Tuple, Union

from warg import Number, drop_unused_kws


def identity(a: Any) -> Any:
  """
    """
  return a


@drop_unused_kws
def kws_sink(*args) -> Tuple[Any, ...]:
  """
    Returns args without any modification what so ever. Drops kws
    :param x:
    :return:"""
  return args


def call_identity(*args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
  """

    :param args:
    :param kwargs:
    :return:"""
  return args, kwargs


# noinspection PyUnusedLocal
def args_sink(*args, **kwargs) -> Dict[str, Any]:
  """

    :param args:
    :param kwargs:
    :return:"""
  return kwargs


# noinspection PyUnusedLocal
def sink(*args, **kwargs) -> None:
  """
    Returns None, but accepts everything

    :param args:
    :param kwargs:
    :return:"""
  return None


def prod(iterable: Iterable[Number]) -> Number:
  """
    Calculate the product of the a Iterable of int or floats
    :param iterable:
    :return:"""
  return reduce(operator.mul, iterable, 1)


def collate_first_dim(batch: Iterable) -> Tuple:
  """

    :param batch:
    :return:"""
  return tuple(zip(*batch))
