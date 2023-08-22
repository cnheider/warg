import itertools
from typing import Optional, Iterator

__all__ = ["peek"]


def peek(generator: Iterator) -> Optional[itertools.chain]:
    try:
        return itertools.chain((next(generator),), generator)
    except StopIteration:
        return None


if __name__ == "__main__":
    print(peek(iter(range(0))))
    print(peek(iter(range(1))))
