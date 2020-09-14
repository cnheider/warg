import time

import numpy
from benchmarks.benchmark_func import benchmark_func
from warg.pooled_queue_processor import PooledQueueProcessor, PooledQueueTask


class Zeroes(PooledQueueTask):
  def call(self, batch_size, *args, tensor_size=(9, 9, 9, 9), **kwargs):
    batch = [(numpy.zeros(tensor_size), i) for i in range(batch_size)]
    imgs = numpy.array([i[0] for i in batch], dtype=numpy.float32)
    ground_truth = numpy.array([i[1] for i in batch], dtype=numpy.float32)
    return (imgs, ground_truth)


Lamb = lambda a, tensor_size:f"{a, tensor_size}"


def Func(a, tensor_size):
  return f"{a, tensor_size}"


def pqp_benchmark():
  task = Zeroes()
  # task = Lamb #Error: cant be pickled
  # task = Func
  batch_size = 16
  tensor_size = (9, 9, 9, 9, 9)
  wait_time = 0.1
  samples = 100

  df = PooledQueueProcessor(
      task, args=[batch_size], kwargs={"tensor_size":tensor_size}, max_queue_size=samples
      )

  def get():
    return df.get()

  def wait_get():
    time.sleep(wait_time)
    return df.get()

  def generate():
    return task(batch_size, tensor_size=tensor_size)

  def wait_generate():
    time.sleep(wait_time)
    return task(batch_size, tensor_size=tensor_size)

  for func, discount in zip(
      (get, wait_get, generate, wait_generate), (0, samples * wait_time, 0, samples * wait_time)
      ):
    t, res = benchmark_func(func, samples)
    print(f"{func.__name__}: {t - discount} seconds")


if __name__ == "__main__":
  pqp_benchmark()
