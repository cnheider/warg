from collections import namedtuple
from typing import Dict, List, Tuple

import sorcery

from benchmarks.benchmark_func import benchmark_func
from warg import NamedOrderedDictionary
from warg.data_structures.named_ordered_dictionary import NOD


def returns_benchmark() -> None:
    """
    :rtype: None
    """
    a = 1
    b = 2
    c = 3

    RandomABC = namedtuple("RandomABC", ("a", "b", "c"))

    def implicit_return() -> Tuple[int, int, int]:
        """
        :rtype: None
        """
        return a, b, c

    def list_return() -> List[int]:
        """
        :rtype: None
        """
        return [a, b, c]

    def tuple_return() -> Tuple[int, int, int]:
        """
        :rtype: None
        """
        return (a, b, c)

    def dict_return() -> Dict[str, int]:
        """
        :rtype: None
        """
        return {"a": a, "b": b, "c": c}

    def sorcery_return() -> None:
        """
        :rtype: None
        """
        return sorcery.dict_of(a, b, c)

    def nod_return() -> NamedOrderedDictionary:
        """
        :rtype: None
        """
        return NOD(a=a, b=b, c=c)

    def inferred_return() -> None:
        """
        :rtype: None
        """
        return NOD.nod_of(a, b, c)

    def namedtuple_return() -> RandomABC:
        """
        :rtype: None
        """
        return RandomABC(a, b, c)

    for func in (
        implicit_return,
        list_return,
        tuple_return,
        dict_return,
        namedtuple_return,
        nod_return,
        sorcery_return,
        inferred_return,
    ):
        t, res = benchmark_func(func)
        print(f"{func.__name__}: {t} seconds, {res}")


if __name__ == "__main__":
    returns_benchmark()
