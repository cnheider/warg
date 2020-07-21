#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/07/2020
           """


__all__ = ["ContextWrapper"]
import inspect


class ContextWrapper:
    """
  Allows for conditional application of contexts, if uninstanted context manager classes are passed no arguments is supplied in construction.
  if disabled None is returned
  if enabled return of context manager is propagated
  """

    def __init__(self, context_manager: callable, enabled: bool):
        self._context_manager = context_manager
        self._enabled = enabled

    def __enter__(self):
        if self._enabled:
            if inspect.isclass(self._context_manager):
                self._context_manager = self._context_manager()

            return self._context_manager.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._enabled:
            return self._context_manager.__exit__(exc_type, exc_val, exc_tb)


if __name__ == "__main__":

    class SampleContextManager:
        def __init__(self, message="Hello World"):
            self._message = message

        def __enter__(self):
            print(self._message)

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(not self._message)  # False ;)

    def main():
        with ContextWrapper(SampleContextManager(), True):
            print("with enabled")

        print()
        with ContextWrapper(SampleContextManager(), False):
            print("with disabled")

        print()
        with ContextWrapper(SampleContextManager, True):
            print("with enabled, uninstantiated")

    main()
