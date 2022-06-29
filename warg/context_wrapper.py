#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/07/2020
           """

__all__ = ["ContextWrapper", "NopContext"]

import contextlib
import inspect
from typing import Callable, Sequence


class NopContext(contextlib.AbstractContextManager):
    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


class ContextWrapper(contextlib.AbstractContextManager):
    """
    Allows for conditional application of contexts, if uninstantiated context manager classes are passed no arguments is supplied in construction.
    if disabled None is returned
    if enabled return of context manager is propagated"""

    def __init__(
        self,
        context_manager: callable,
        enabled: bool,
        construction_args: Sequence = (),
        construction_kwargs=None,
    ):
        if construction_kwargs is None:
            construction_kwargs = {}

        self._context_manager = context_manager
        self._enabled = enabled
        self._construction_args = construction_args
        self._construction_kwargs = construction_kwargs

    def __enter__(self):
        if self._enabled:
            if inspect.isclass(self._context_manager) or isinstance(self._context_manager, Callable):
                self._context_manager = self._context_manager(
                    *self._construction_args, **self._construction_kwargs
                )
            if hasattr(self._context_manager, "__enter__"):
                return self._context_manager.__enter__()
            else:
                raise NotImplementedError(f"{self._context_manager} does not implement __enter__")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._enabled:
            return self._context_manager.__exit__(exc_type, exc_val, exc_tb)


if __name__ == "__main__":

    class SampleContextManager:
        """description"""

        def __init__(self, message="Hello World"):
            self._message = message

        def __enter__(self):
            print(self._message)

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(not self._message)  # False ;)

    def main() -> None:
        """
        :rtype: None
        """
        with ContextWrapper(SampleContextManager(), True):
            print("with enabled")

        print()
        with ContextWrapper(SampleContextManager(), False):
            print("with disabled")

        print()
        with ContextWrapper(SampleContextManager, True):
            print("with enabled, uninstantiated")

    main()
