#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod

__author__ = 'cnheider'

import multiprocessing as mp
import queue


class PooledQueueTask(object):

  def __call__(self, *args, **kwargs):
    return self.call(*args, **kwargs)

  @abstractmethod
  def call(self, *args, **kwargs):
    raise NotImplemented


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

  @property
  def kwargs(self):
    return self._kwargs

  @kwargs.setter
  def kwargs(self, value):
    self._kwargs = value

  @property
  def args(self):
    return self.args

  @args.setter
  def args(self, value):
    self._args = value

  def maybe_fill(self):
    if self.queue_size < self._max_size:
      self._pool.apply_async(self._func, self._args, self._kwargs, self.put, self.error)

  @property
  def queue_size(self):
    return self._queue.qsize()

  def put(self, res):
    self._queue.put(res)

  def error(self, error):
    raise error

  def get(self):
    res = self._queue.get()
    self.maybe_fill()
    return res

  def __len__(self):
    return self.queue_size

  def __iter__(self):
    return self

  def __next__(self):
    return self.get()


if __name__ == '__main__':

  class Square(PooledQueueTask):

    def call(self, i, *args, **kwargs):
      return i * 2


  class Exc(PooledQueueTask):

    def call(self, *args, **kwargs):
      raise NotImplementedError


  task = Square()

  df = PooledQueueProcessor(task, 2)
  for a, _ in zip(df, range(30)):
    print(a)

  df.args = [4]

  for a, _ in zip(df, range(30)):
    print(a)
