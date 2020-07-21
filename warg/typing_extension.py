#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 18/07/2020
           """

import numbers
from typing import Sequence, Union


__all__ = ["Number", "Reals", "Numbers", "StrictNumbers"]

Number = Union[int, float]
Reals = Sequence[Union[numbers.Real, "Reals"]]
Numbers = Sequence[Union[Number, "Numbers"]]
StrictNumbers = Union[Union[Sequence[int], "StrictNumbers"], Union[Sequence[float], "StrictNumbers"]]

if __name__ == "__main__":

    def stest():
        assert (
            isinstance(1, Number.__args__)
            and isinstance(1.1, Number.__args__)
            and not isinstance(complex(1, 1), Number.__args__)
        )
        # assert isinstance(list(range(2)), Numbers.__args__) and isinstance((float(i) for i in range(2)), Numbers.__args__) and isinstance((1,2.0), Numbers.__args__)
        # assert isinstance(list(range(2)), StrictNumbers.__args__) and isinstance((float(i) for i in range(2)), StrictNumbers.__args__) and not isinstance((1,2.0), StrictNumbers.__args__)
        assert (
            isinstance(1, numbers.Real)
            and isinstance(1.1, numbers.Real)
            and not isinstance(complex(2, 2), numbers.Real)
        )
        # assert isinstance(list(range(2)), Reals.__args__) and isinstance((float(i) for i in range(2)), Reals.__args__) and isinstance((1,2.0), Reals.__args__)

    stest()
