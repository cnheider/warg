#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 09-02-2021
           """
__all__ = ["IgnoreInterruptSignal", "LambdaContext"]

import contextlib
import signal

from warg import AlsoDecorator


class LambdaContext(contextlib.AbstractContextManager):
    def __init__(self, callable_):
        self.callable_ = callable_

    def __enter__(self):
        return self.callable_

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __getattr__(self, item):
        return getattr(iter, self.callable_)

    def __getitem__(self, item):
        return self.callable_[item]

    def __call__(self, *args, **kwargs):
        return self.callable_


class IgnoreInterruptSignal(contextlib.AbstractContextManager, AlsoDecorator):
    """description"""

    def __enter__(self) -> bool:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # signal.getsignal() No sideeffect options for exit
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
