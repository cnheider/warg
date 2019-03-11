#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import multiprocessing as mp
import queue
import traceback

import numpy as np


class PooledQueueTask(object):

  def task(self, i):
    return (np.zeros((999, 999)), i)

  def generate_batch(self, batch_size):
    try:
      batch = [self.task(i) for i in range(batch_size)]
      imgs = np.array([i[0] for i in batch], dtype=np.float32)
      ground_truth = np.array([i[1] for i in batch], dtype=np.float32)
      return (imgs, ground_truth)
    except Exception as inst:
      traceback.print_exc()
      return inst


class PooledQueueProcessor(object):
  '''
      This is a workaround of Pythons extremely slow interprocess communication pipes.
      The ideal solution would be to use a multiprocessing.queue, but it apparently communication is band
      limited.
      This solution has processes complete tasks (batches) and a thread add the results to a queue.queue.
  '''

  def __init__(self, func, *args, max_size=6, n_proc=2, max_tasks_per_child=3, **kwargs):
    self._max_size = max_size
    self._func = func
    self._args = args
    self._kwargs = kwargs

    self._queue = queue.Queue(maxsize=max_size)
    self._pool = mp.Pool(n_proc, maxtasksperchild=max_tasks_per_child)

    for i in range(max_size):
      self.maybe_fill()

  def close(self):
    self._pool.close()
    self._pool.join()

  def terminate(self):
    self._pool.terminate()
    self._pool.join()

  def maybe_fill(self):
    if self.queue_size < self._max_size:
      self._pool.apply_async(self._func, self._args, self._kwargs, self.put)

  @property
  def queue_size(self):
    return self._queue.qsize()

  def put(self, *args, **kwargs):
    if isinstance(args[0], Exception):
      raise args[0]
    self._queue.put(*args, **kwargs)

  def get(self, *args, **kwargs):
    res = self._queue.get(*args, **kwargs)
    self.maybe_fill()
    return res

  def __len__(self):
    return self.queue_size

  def __iter__(self):
    return self

  def __next__(self):
    return self.get()


if __name__ == '__main__':
  from functools import partial

  pqt = PooledQueueTask()

  batch_size = 64
  bas = partial(pqt.generate_batch, batch_size)

  df = PooledQueueProcessor(bas)
  for a, _ in zip(df, range(30)):
    print(a)
