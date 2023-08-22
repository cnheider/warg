from typing import Sequence, Any, Tuple

__all__ = ["pairs", "chunks"]


def pairs(s: Sequence) -> Tuple[Any, Any]:
    """
    Iterate over a list in overlapping pairs.

    Usage:
        lst = [4, 7, 11, 2]
        pairs(lst) yields (4, 7), (7, 11), (11, 2)

    https://stackoverflow.com/questions/1257413/1257446#1257446


    :param s: An iterable/list
    :return: Yields a pair of consecutive elements (lst[k], lst[k+1]) of lst. Last call yields (lst[-2], lst[-1]).
    """
    i = iter(s)
    prev = next(i)

    for item in i:
        yield prev, item
        prev = item


def chunks(lst: Sequence, n: int) -> Any:
    """
    Yield successive n-sized chunks from lst.

     :param lst:
     :param n:
     :return:
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    print(list(chunks(list(range(10)), 3)))
