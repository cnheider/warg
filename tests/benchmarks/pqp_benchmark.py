import time
from functools import partial

from benchmark_func import benchmark_func
from warg.pooled_queue_processor import PooledQueueProcessor, PooledQueueTask


def pqp_benchmark():
  pqt = PooledQueueTask()
  batch_size = 12

  bas = partial(pqt.generate_batch, batch_size)
  df = PooledQueueProcessor(bas, max_size=batch_size)

  def d():
    return df.get()

  def c():
    time.sleep(1)
    return df.get()

  def a():
    return pqt.generate_batch(batch_size)

  def aa():
    time.sleep(1)
    return pqt.generate_batch(batch_size)

  for func in (d,
               c,
               a,
               aa):
    t, res = benchmark_func(func,10)
    print(f'{func.__name__}: {t} seconds')


if __name__ == '__main__':
  pqp_benchmark()
