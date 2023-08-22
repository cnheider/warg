import random
from typing import Iterable, Tuple, Callable, List

from warg import Number

__all__ = ["n_uint_mix", "n_uint_mix_generator_builder", "n_uint_mix_generator"]


def n_uint_mix(mix: Iterable[Number]) -> List[Number]:
    return [random.randrange(0, m) for m in mix]


def n_uint_mix_generator(*mix) -> Tuple[Number, ...]:
    if len(mix) == 1:
        if isinstance(mix, Iterable):
            mix = mix[0]

    while 1:
        yield n_uint_mix(mix)


def n_uint_mix_generator_builder(*mix: Number) -> Callable:
    """Compatability code.."""

    if len(mix) == 1:
        if isinstance(mix, Iterable):
            mix = mix[0]

    def no_arg_generator() -> Tuple[Number, ...]:
        while 1:
            yield n_uint_mix(mix)

    return no_arg_generator


if __name__ == "__main__":
    print([v for _, v in zip(range(9), iter(n_uint_mix_generator(255, 255)))])
