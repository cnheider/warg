#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 09-09-2020
           """

__all__ = [
    "map_value_product",
    "map_product",
    "map_permutations",
    "map_combinations",
    "map_combinations_with_replacement",
]

import itertools
from typing import Any, Mapping, Tuple


def map_value_product(dicts: Mapping) -> Any:
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))


def map_product(dicts: Mapping, r: int = 2) -> Any:
    yield from zip(
        itertools.product(dicts.keys(), repeat=r),
        itertools.product(dicts.values(), repeat=r),
    )


def map_permutations(dicts: Mapping, r: int = 2) -> Tuple:
    yield from zip(
        itertools.permutations(dicts.keys(), r),
        itertools.permutations(dicts.values(), r),
    )


def map_combinations(dicts: Mapping, r: int = 2) -> Tuple:
    yield from zip(
        itertools.combinations(dicts.keys(), r),
        itertools.combinations(dicts.values(), r),
    )


def map_combinations_with_replacement(dicts: Mapping, r: int = 2) -> Tuple:
    yield from zip(
        itertools.combinations_with_replacement(dicts.keys(), r),
        itertools.combinations_with_replacement(dicts.values(), r),
    )


if __name__ == "__main__":

    def asdijha():
        from warg import NOD

        a = NOD(a=[1], b=[4], c=[8])
        print(f"ValueMapProduct{str(list(map_value_product(a.as_dict())))}")
        print(f"MapProduct{str(list(map_product(a.as_dict())))}")
        print(f"map_combinations{str(list(map_combinations(a.as_dict())))}")
        print(f"map_permutations{str(list(map_permutations(a.as_dict())))}")
        print(
            f"map_combinations_with_replacement{str(list(map_combinations_with_replacement(a.as_dict())))}"
        )

    def asdijhsadasdad():
        from warg import NOD

        a = NOD(a=[1, 2, 8], b=[4, 3, 99])
        print(f"ValueMapProduct{str(list(map_value_product(a.as_dict())))}")
        print(f"MapProduct{str(list(map_product(a.as_dict())))}")
        print(f"map_combinations{str(list(map_combinations(a.as_dict())))}")
        print(f"map_permutations{str(list(map_permutations(a.as_dict())))}")
        print(
            f"map_combinations_with_replacement{str(list(map_combinations_with_replacement(a.as_dict())))}"
        )

    asdijha()
    # asdijhsadasdad()
