import time
from functools import partial
import numpy as np

from benchmarks.benchmark_func import benchmark_func
from warg.pooled_queue_processor import PooledQueueProcessor, PooledQueueTask


def pqp_benchmark():
  class Zeroes(PooledQueueTask):

    def call(self, batch_size, *args, **kwargs):
      batch = [(np.zeros((99, 99)), i) for i in range(batch_size)]
      imgs = np.array([i[0] for i in batch], dtype=np.float32)
      ground_truth = np.array([i[1] for i in batch], dtype=np.float32)
      return (imgs, ground_truth)

  pqt = Zeroes()

  batch_size = 12

  bas = partial(pqt, batch_size)
  df = PooledQueueProcessor(bas, max_size=batch_size)

  def d():
    return df.get()

  def c():
    time.sleep(0.1)
    return df.get()

  def a():
    return pqt(batch_size)

  def aa():
    time.sleep(0.1)
    return pqt(batch_size)

  for func in (d,
               c,
               a,
               aa):
    t, res = benchmark_func(func, 10)
    print(f'{func.__name__}: {t} seconds')

if __name__ == '__main__':
  pqp_benchmark()
