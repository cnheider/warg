import itertools
from math import sin, cos
from typing import Iterable

from warg import Number

__all__ = ["sin_gen", "cos_gen", "loop"]

loop = itertools.cycle


def sin_gen(iterable: Iterable[Number], magnitude: Number = 1) -> Iterable[Number]:
    """

    :param magnitude:
    :type magnitude:
    :param iterable:
    :type iterable:"""
    for a in iterable:
        yield sin(a) * magnitude


def cos_gen(iterable: Iterable[Number], magnitude: Number = 1) -> Iterable[Number]:
    """

    :param magnitude:
    :type magnitude:
    :param iterable:
    :type iterable:"""
    for a in iterable:
        yield cos(a) * magnitude


if __name__ == "__main__":

    def assda():
        """description"""
        import numpy

        for i in cos_gen(numpy.arange(0, 100, 0.1)):
            print(i)

    assda()
