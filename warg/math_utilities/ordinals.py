import math

from warg.typing_extension import Number

__all__ = [
    "ceil_odd",
    "ceil_even",
    "floor_even",
    "floor_odd",
    "next_even",
    "next_odd",
    "prev_even",
    "prev_odd",
]


def ceil_even(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return math.ceil(v / 2.0) * 2


def floor_even(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return math.floor(v / 2.0) * 2


def ceil_odd(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return math.ceil(v) // 2 * 2 + 1


def floor_odd(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    v = math.floor(v)
    return v + v % 2 - 1


def next_even(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return floor_even(v) + 2


def next_odd(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return floor_odd(v) + 2


def prev_even(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return ceil_even(v) - 2


def prev_odd(v: Number) -> Number:
    """

    :param v:
    :type v:
    :return:
    :rtype:
    """
    return ceil_odd(v) - 2


if __name__ == "__main__":
    from warg.ast_ops import cprint
    import numpy

    for a in numpy.arange(-1.0, 10.0, 0.5):
        cprint(a)
        for f in (
            ceil_odd,
            ceil_even,
            floor_even,
            floor_odd,
            next_even,
            next_odd,
            prev_even,
            prev_odd,
        ):
            print(f.__name__, f(a))
