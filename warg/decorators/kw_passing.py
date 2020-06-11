#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import inspect
import types
from functools import wraps
from logging import warning
from typing import Dict, Tuple

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
          The concept "kw passing" implemented here lets one make a contract with the caller that all
          kwargs with be passed onwards to a receiver, this lets the caller inspect available kwargs of the
          the receiver function allowing for autocompletion, typing and documentation fetching.
           """

__all__ = [
    "passes_kws_to",
    "super_init_pass_on_kws",
    "drop_unused_kws",
    "drop_unused_args",
    "drop_kws",
    "drop_args",
    "AlsoDecorator",
]


def to_keyword_only(val: inspect.Parameter) -> inspect.Parameter:
    """

    :param val:
    :type val:
    :return:
    :rtype:
    """
    if val._kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
        val._kind = inspect._ParameterKind.KEYWORD_ONLY
    return val


def eval_sig_kw_params(
    passing_sig: inspect.Signature, receiver_func: callable, keep_from_var_kw: bool = False
) -> Tuple[inspect.Signature, Dict[str, inspect.Parameter]]:
    """

    :param passing_sig:
    :type passing_sig:
    :param receiver_func:
    :type receiver_func:
    :param keep_from_var_kw:
    :type keep_from_var_kw:
    :return:
    :rtype:
    """
    passing_params: dict = dict(passing_sig.parameters)
    receiver_params = inspect.signature(receiver_func).parameters

    var_kw_key = None
    var_kw = None
    for k, v in passing_params.items():
        if v.kind == inspect._ParameterKind.VAR_KEYWORD:
            var_kw_key = k

    if var_kw_key in passing_params:
        var_kw = passing_params.pop(var_kw_key)

    to_params = {
        key: to_keyword_only(val)
        for key, val in receiver_params.items()
        if val.default != inspect.Parameter.empty and key not in passing_params
    }

    passing_params.update(to_params)

    if keep_from_var_kw:
        passing_params[var_kw_key] = var_kw

        no_var_kw = True
        for k, v in receiver_params.items():
            if v.kind == inspect._ParameterKind.VAR_KEYWORD:
                no_var_kw = False
        if no_var_kw:
            warning(
                f"Receiver {receiver_func} with {receiver_params} does not acceptable arbitrary kwargs although "
                f"from_func will pass "
                f"all "
                f"kwargs onwards TypeErrors might occur, to fix this let this receiver accept any arbitrary "
                f"kwargs by adding ..,**kwargs): to the receivers function declaration"
            )

    return passing_sig, passing_params


def passes_kws_to(*receiver_funcs: callable, keep_from_var_kw: bool = False) -> callable:
    """
A contract decorator, attaching this to a function you explicitly state that kws will be passed onward to
a receiver function. No call graph checks if this actually enforces this yet. Also all receiver kwargs
must be able to be received by receivers if multiple contracts are use

:param receiver_funcs:
:param keep_from_var_kw:
:return:
"""
    for receiver_func in receiver_funcs:
        if isinstance(receiver_func, types.BuiltinFunctionType):
            raise AssertionError(f"'Built In Receiver' function: {receiver_func}, is not supported")

    def _func(passing_func: callable) -> callable:
        passing_sig = inspect.signature(passing_func)
        for receiver_func in receiver_funcs:
            passing_sig, new_params = eval_sig_kw_params(passing_sig, receiver_func, keep_from_var_kw)
            passing_sig = passing_sig.replace(parameters=new_params.values())
        passing_func.__signature__ = passing_sig
        return passing_func

    return _func


def super_init_pass_on_kws(
    f: callable = None, *, super_base: type = None, keep_from_var_kw: bool = False
) -> callable:
    """

:param f:
:param super_base:
:param keep_from_var_kw:
:return:
"""

    def _func(func):
        if super_base:
            to_func = super_base.__init__
        else:
            to_func = inspect.getmro(func)[0].__init__

        from_func = func.__init__

        from_sig = inspect.signature(from_func)
        from_signature, signature_parameters = eval_sig_kw_params(from_sig, to_func, keep_from_var_kw)
        from_func.__signature__ = from_signature.replace(parameters=signature_parameters.values())
        return func

    if f:
        return _func(f)

    return _func


def drop_args(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kws):
        """

        :param args:
        :type args:
        :param kws:
        :type kws:
        :return:
        :rtype:
        """
        return f(**kws)

    return wrapper


def drop_kws(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kws):
        """

        :param args:
        :type args:
        :param kws:
        :type kws:
        :return:
        :rtype:
        """
        return f(*args)

    return wrapper


def drop_unused_args(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kws):
        """

        :param args:
        :type args:
        :param kws:
        :type kws:
        :return:
        :rtype:
        """
        return f(**kws)

    return wrapper


def drop_unused_kws(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kws):
        """

        :param args:
        :type args:
        :param kws:
        :type kws:
        :return:
        :rtype:
        """
        from_sig = inspect.signature(f)

        for k, v in from_sig.parameters.items():
            if v.kind == inspect._ParameterKind.VAR_KEYWORD:
                return f(*args, **kws)

        kept = {}
        for k, v in kws.items():
            if k in from_sig.parameters.keys():
                kept[k] = v

        return f(*args, **kept)

    return wrapper


class AlsoDecorator:
    def __call__(self, func):
        @functools.wraps(func)
        def decorate_no_grad(*args, **kwargs):
            """

      :param args:
      :type args:
      :param kwargs:
      :type kwargs:
      :return:
      :rtype:
      """
            with self:
                return func(*args, **kwargs)

        return decorate_no_grad


if __name__ == "__main__":

    class BaseClass:
        """

        """

        def __init__(self, arg0, *args, kwarg0=None, kwarg1=None, **kwargs):
            self.arg0 = arg0
            for key, val in enumerate(args):
                setattr(self, f"arg{key + 1}", val)
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1
            self.__dict__.update(kwargs)

    class SubClass0(BaseClass):
        """

        """

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs):
            super().__init__(arg0, *args, **kwargs)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """

        """

        def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs):
            super().__init__(arg0, *args, **kwargs)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws(super_base=BaseClass)
    class SubClass2(BaseClass):
        """

        """

        def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs):
            super().__init__(arg0, *args, **kwargs)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @drop_unused_kws
    def some_func(*, a):
        """

        :param a:
        :type a:
        """
        print(a)

    @drop_unused_kws
    def some_other_func(*, a, **kwargs):
        """

        :param a:
        :type a:
        :param kwargs:
        :type kwargs:
        """
        print(a, kwargs)

    @drop_unused_kws
    def some_different_func(*, a, b):
        """

        :param a:
        :type a:
        :param b:
        :type b:
        """
        print(a, b)

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))
    print(vars(SubClass2(1, 1, 1, kwarg0=52)))
    print(inspect.getmro(SubClass0))

    some_func(a=1, b=2, c=3)

    some_other_func(a=1, b=2)

    some_different_func(a=1, c=2, b="l")
