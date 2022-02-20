from math import sin, cos
from typing import Iterable

from warg import Number

__all__ = ["sin_gen", "cos_gen"]


def sin_gen(iterable: Iterable[Number], magnitude: Number = 1) -> Iterable[Number]:
    """

    :param func:
    :type func:
    :param kw:
    :type kw:
    :param iterable:
    :type iterable:"""
    for a in iterable:
        yield sin(a) * magnitude


def cos_gen(iterable: Iterable, magnitude: Number = 1) -> Iterable[Number]:
    """

    :param func:
    :type func:
    :param kw:
    :type kw:
    :param iterable:
    :type iterable:"""
    for a in iterable:
        yield cos(a) * magnitude


if __name__ == "__main__":

    def assda():
        import numpy

        for i in cos_gen(numpy.arange(0, 100, 0.1)):
            print(i)

    assda()
