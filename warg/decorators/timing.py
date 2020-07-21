#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/11/2019
           """

__all__ = ["timeit", "StopWatch"]

import contextlib
import functools
import time
import typing
from functools import wraps


def timeit(f: callable):
    """

  :param f:
  :type f:
  :return:
  :rtype:
  """

    @wraps(f)
    def wrapper(*args, **kwds):
        """

    :param args:
    :type args:
    :param kwds:
    :type kwds:
    :return:
    :rtype:
    """
        start_time = time.time()
        result = f(*args, **kwds)
        elapsed_time = time.time() - start_time
        print(f"{f} took {elapsed_time:.3f} seconds to compute")
        return elapsed_time, result

    return wrapper


class StopWatch(contextlib.AbstractContextManager):
    r"""**Measure execution time of function.**

  Can be used as context manager or function decorator, perform checkpoints
  or display absolute time from measurements beginning.

  **Used as context manager**::

      with Timer() as timer:
          ... # your operations
          print(timer) # __str__ calls timer.time() internally
          timer.checkpoint() # register checkpoint
          ... # more operations
          print(timer.checkpoint()) # time since last timer.checkpoint() call

      ... # even more operations
      print(timer) # time taken for the block, will not be updated outside of it

  When execution leaves the block, timer will be blocked. Last checkpoint and time taken
  to execute whole block will be returned by `checkpoint()` and `time()` methods respectively.

  **Used as function decorator**::

      @Timer()
      def foo():
          return 42

      value, time = foo()

  Parameters
  ----------
  function : Callable, optional
          No argument function used to measure time. Default: time.perf_counter

  """

    def __init__(
        self,
        function: typing.Callable = time.perf_counter,
        auto_start_on_construction: bool = False,
        auto_start_on_enter: bool = True,
        auto_stop_on_exit: bool = True,
    ):
        self._stopped: bool = False
        self._started = False

        self._callable = function
        self._auto_start_on_construction = auto_start_on_construction
        self._auto_start_on_enter = auto_start_on_enter
        self._auto_stop_on_exit = auto_stop_on_exit

        self.start_time = 0
        self.new_time = 0
        self.previous_time = 0

        if self._auto_start_on_construction:
            self.start_timer()

        self.override_arithmetics()

    def override_arithmetics(self):
        def make_func(name):
            return lambda self, *args: getattr(self.since_start, name)(*args)

        arithmetics = ("add", "sub", "mul", "div", "truediv", "floordiv", "mod", "divmod", "pow")

        methods = [
            "__invert__",
            "__neg__",
            "__pos__",
            "abs",
            "__round__",
            "__floor__",
            "__ceil__",
            "__int__",
            "__float__",
        ]
        methods.extend([f"__{n}__" for n in arithmetics])
        methods.extend([f"__r{n}__" for n in arithmetics])
        methods.extend([f"__i{n}__" for n in arithmetics])

        for name in methods:
            setattr(StopWatch, name, make_func(name))

    def start_timer(self):
        self._started = True
        self.start_time = self._callable()
        self.new_time = self.start_time
        self.previous_time = self.start_time

    def stop_timer(self):
        self.new_time = self._callable()
        self._stopped: bool = True

    @property
    def since_start(self):
        """**Time taken since the start of timer (measurements beginning).**

    Returns
    -------
    time-like
            Whatever `self.function() - self.function()` returns,
            usually fraction of seconds
    """
        if not self._stopped and self._started:
            return self._callable() - self.start_time
        return self.new_time - self.start_time

    def tick(self):
        """**Time taken since last tick call.**

    If wasn't called before, it is the same as as Timer creation time (first call returns
    the same thing as `time()`)

    Returns
    -------
    time-like
            Whatever `self.function() - self.function()` returns,
            usually fraction of seconds
    """
        if not self._stopped:
            if self._started:
                self.previous_time = self.new_time
                self.new_time = self._callable()
            else:
                self.start_timer()
        return self.new_time - self.previous_time

    def __call__(self, function):
        """
    decorator functionality

    :param function:
    :type function:
    :return:
    :rtype:
    """

        @functools.wraps(function)
        def decorated(*args, **kwargs):
            self.start_timer()
            values = function(*args, **kwargs)
            self.stop_timer()
            return values, self.since_start

        return decorated

    def __enter__(self):
        if self._auto_start_on_enter:
            self.start_timer()
        return self

    def __exit__(self, *_, **__) -> None:
        if self._auto_stop_on_exit:
            self.stop_timer()
        return False

    def __str__(self) -> str:
        return str(self.__repr__())

    def __repr__(self):
        return self.since_start


if __name__ == "__main__":

    a = StopWatch()
    print(f"Timer str rep: {a}")
    print(a.tick())
    print(a.tick())
    print(a // 2)
    print()

    with StopWatch(auto_start_on_enter=False) as timer1:
        print(timer1)  # __str__ calls timer.time() internally
        timer1.tick()  # register checkpoint
        print(timer1.tick())  # time since last timer.checkpoint() call

    print()
    with StopWatch() as timer4:
        print(timer4)  # __str__ calls timer.time() internally
        timer4.tick()  # register checkpoint
        print(timer4.tick())  # time since last timer.checkpoint() call

    print()
    print(timer4)  # time since start
    print(timer4.tick())  # time taken for the block, will not be updated outside of it
    print(timer4.tick())  # time taken for the block, will not be updated outside of it
    print(timer4)  # ime since start, will not be updated outside of it
    print()

    with StopWatch(auto_start_on_construction=True, auto_start_on_enter=False) as timer2:
        print(timer2)  # __str__ calls timer.time() internally
        print(timer2.tick())  # time since last timer.checkpoint() call
        print(timer2)

    @StopWatch()
    def foo():
        return 42

    value, time = foo()
    print(f"foo time: {time}, value: {value}")
