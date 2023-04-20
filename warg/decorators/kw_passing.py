#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import inspect
import types
from functools import wraps
from logging import warning
from typing import Dict, MutableMapping, Sequence, Tuple, Any

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
    "drop_args_and_kws",
    "pack_args",
    "pack_kws",
    "pack_args_and_kws",
    "AlsoDecorator",
]


# noinspection PyUnresolvedReferences
def to_keyword_only(val: inspect.Parameter) -> inspect.Parameter:
    """

    :param val:
    :type val:
    :return:
    :rtype:"""
    if val._kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
        val._kind = inspect._ParameterKind.KEYWORD_ONLY
    return val


# noinspection PyUnresolvedReferences
def eval_sig_kw_params(
    passing_sig: inspect.Signature,
    receiver_func: callable,
    keep_from_var_kw: bool = False,
) -> Tuple[inspect.Signature, Dict[str, inspect.Parameter]]:
    """

    :param passing_sig:
    :type passing_sig:
    :param receiver_func:
    :type receiver_func:
    :param keep_from_var_kw:
    :type keep_from_var_kw:
    :return:
    :rtype:"""
    passing_params: dict = dict(passing_sig.parameters)
    # if inspect.isfunction()
    # if inspect.ismethod()
    # arg_spec_sig = inspect.getfullargspec(receiver_func)[0]

    receiver_params = inspect.signature(
        receiver_func
    ).parameters  # TODO: Sometime no signature is found resulting in
    # a ValueError exception

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
    :return:"""
    for receiver_func in receiver_funcs:
        if isinstance(receiver_func, types.BuiltinFunctionType):
            raise AssertionError(f"'Built In Receiver' function: {receiver_func}, is not supported")

    def _func(passing_func: callable) -> callable:
        passing_sig = inspect.signature(passing_func)
        for rf in receiver_funcs:
            passing_sig, new_params = eval_sig_kw_params(passing_sig, rf, keep_from_var_kw)
            passing_sig = passing_sig.replace(parameters=list(new_params.values()))
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
    :return:"""

    def _func(func) -> callable:
        if super_base:
            to_func = super_base.__init__
        else:
            to_func = inspect.getmro(func)[0].__init__

        from_func = func.__init__

        from_sig = inspect.signature(from_func)
        from_signature, signature_parameters = eval_sig_kw_params(from_sig, to_func, keep_from_var_kw)
        from_func.__signature__ = from_signature.replace(parameters=list(signature_parameters.values()))
        return func

    if f:
        return _func(f)

    return _func


def drop_args(f: callable) -> callable:
    """

    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(f)
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        return f(**kwargs)

    return wrapper


def drop_kws(f: callable) -> callable:
    """

    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(f)
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        return f(*args)

    return wrapper


def drop_args_and_kws(f: callable) -> callable:
    """

    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(f)
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        return f()

    return wrapper


WRAPPER_NO_ANNOTATION = tuple(
    set(functools.WRAPPER_ASSIGNMENTS)
    - {
        "__annotations__",
    }
)


def pack_args(
    f: callable,
    *,
    pack_name: str = "arg_pack",
    allow_passing: bool = True,
    verbose: bool = False,
) -> callable:
    """

    :param pack_name:
    :type pack_name:
    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(
        f,
        # assigned=WRAPPER_NO_ANNOTATION,
        # updated=("__annotations__",),
    )
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        new_kwargs = kwargs.copy()
        if not allow_passing:
            assert pack_name not in kwargs, f"thou shall not pass {pack_name}"
        else:
            if pack_name in kwargs:
                if verbose:
                    print(f"{pack_name} was extended, careful!")
                a = kwargs.pop(pack_name, None)
                new_kwargs[pack_name] = (*a, *args)
            else:
                new_kwargs[pack_name] = args
        return f(*args, **new_kwargs)

    return wrapper


def pack_kws(
    f: callable,
    *,
    pack_name: str = "kw_pack",
    allow_passing: bool = True,
    verbose: bool = False,
) -> callable:
    """

    :param pack_name:
    :type pack_name:
    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(
        f,
        # assigned=WRAPPER_NO_ANNOTATION, #TODO: Figure out if pack_name can be hidden from function signature
        # updated=("__annotations__",),
    )
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        new_kwargs = kwargs.copy()
        if not allow_passing:
            assert pack_name not in kwargs, f"thou shall not pass {pack_name}"
        else:  # TODO: else keyword can be removed, but branch remain
            if pack_name in kwargs:
                if verbose:
                    print(f"{pack_name} was extended, careful!")
                k = kwargs.pop(pack_name, None)
                new_kwargs[pack_name] = {**k, **kwargs}
            else:
                new_kwargs[pack_name] = kwargs
        return f(*args, **new_kwargs)

    return wrapper


def pack_args_and_kws(
    f: callable,
    *,
    pack_name: str = "arg_kw_pack",
    allow_passing: bool = True,
    verbose: bool = False,
) -> callable:
    """

    :param pack_name:
    :type pack_name:
    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(
        f,
        # assigned=WRAPPER_NO_ANNOTATION,
        # updated=("__annotations__",),
    )
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        new_kwargs = kwargs.copy()
        if not allow_passing:
            assert pack_name not in kwargs, f"thou shall not pass {pack_name}"
        else:  # TODO: else keyword can be removed, but branch remain
            if pack_name in kwargs:
                if verbose:
                    print(f"{pack_name} was extended, careful!")
                a, k = kwargs.pop(pack_name, None)
                new_kwargs[pack_name] = ((*a, *args), {**k, **kwargs})
            else:
                new_kwargs[pack_name] = (args, kwargs)
        return f(*args, **kwargs)

    return wrapper


def drop_unused_args(f: callable) -> callable:
    """

    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(f)
    def wrapper(*args, **kwargs: MutableMapping) -> Any:
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        return f(**kwargs)

    return wrapper


# noinspection PyUnresolvedReferences
def drop_unused_kws(f: callable) -> callable:
    """

    :param f:
    :type f:
    :return:
    :rtype:"""

    @wraps(f)
    def wrapper(*args, **kwargs: MutableMapping):
        """

        :param args:
        :type args:
        :return:
        :rtype:"""
        from_sig = inspect.signature(f)

        for k, v in from_sig.parameters.items():
            if v.kind == inspect._ParameterKind.VAR_KEYWORD:
                return f(*args, **kwargs)

        kept = {}
        for k, v in kwargs.items():
            if k in from_sig.parameters.keys():
                kept[k] = v

        return f(*args, **kept)

    return wrapper


class AlsoDecorator:
    """
    Lets you use a function as a decorator too
    """

    def __call__(self, func):
        @functools.wraps(func)
        def decorate_func(*args: Sequence, **kwargs: MutableMapping):
            """

            :param args:
            :type args:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:"""
            with self:
                return func(*args, **kwargs)

        return decorate_func


if __name__ == "__main__":

    def _main():
        class BaseClass:
            """description"""

            def __init__(self, arg0, *args, kwarg0=None, kwarg1=None, **kwargs: MutableMapping):
                self.arg0 = arg0
                for key, val in enumerate(args):
                    setattr(self, f"arg{key + 1}", val)
                self.kwarg0 = kwarg0
                self.kwarg1 = kwarg1
                self.__dict__.update(kwargs)

        class SubClass0(BaseClass):
            """description"""

            @passes_kws_to(BaseClass.__init__)
            def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs: MutableMapping):
                super().__init__(arg0, *args, **kwargs)
                self.arg1 = arg1
                self.arg2 = arg2
                self.kwarg2 = kwarg2

        @super_init_pass_on_kws
        class SubClass1(BaseClass):
            """description"""

            def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs: MutableMapping):
                super().__init__(arg0, *args, **kwargs)
                self.arg1 = arg1
                self.arg2 = arg2
                self.kwarg2 = kwarg2

        @super_init_pass_on_kws(super_base=BaseClass)
        class SubClass2(BaseClass):
            """description"""

            def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs: MutableMapping):
                super().__init__(arg0, *args, **kwargs)
                self.arg1 = arg1
                self.arg2 = arg2
                self.kwarg2 = kwarg2

        @drop_unused_kws
        def some_func(*, a):
            """

            :param a:
            :type a:"""
            print(a)

        @drop_unused_kws
        def some_other_func(*, a, **kwargs: MutableMapping):
            """

            :param a:
            :type a:
            :param kwargs:
            :type kwargs:"""
            print(a, kwargs)

        @drop_unused_kws
        def some_different_func(*, a, b):
            """

            :param a:
            :type a:
            :param b:
            :type b:"""
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

    _main()
