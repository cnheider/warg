from collections import namedtuple

import sorcery
from benchmarks.benchmark_func import benchmark_func
from warg.data_structures.named_ordered_dictionary import NOD


def returns_benchmark():
  a = 1
  b = 2
  c = 3

  RandomABC = namedtuple("RandomABC", ("a", "b", "c"))

  def implicit_return():
    return a, b, c

  def list_return():
    return [a, b, c]

  def tuple_return():
    return (a, b, c)

  def dict_return():
    return {"a":a, "b":b, "c":c}

  def sorcery_return():
    return sorcery.dict_of(a, b, c)

  def nod_return():
    return NOD(a=a, b=b, c=c)

  def inferred_return():
    return NOD.nod_of(a, b, c)

  def namedtuple_return():
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
