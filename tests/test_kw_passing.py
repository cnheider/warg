#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
from typing import Sequence, MutableMapping

from warg.decorators.kw_passing import (
    drop_unused_kws,
    passes_kws_to,
    super_init_pass_on_kws,
)

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
           """


def test_subclass_fully_qualified_no_args_or_kwargs():
    class BaseClass:
        """description"""

        def __init__(self, arg0, kwarg0=None, kwarg1=None):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_with_args_and_kwargs_on_subclasses():
    class BaseClass:
        """description"""

        def __init__(self, arg0, *args, kwarg0=None, kwarg1=None, **kwargs: MutableMapping):
            """

            :param arg0:
            :param args:
            :param kwarg0:
            :param kwarg1:
            :param kwargs:"""
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

    @super_init_pass_on_kws()
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, *args, kwarg2=None, **kwargs: MutableMapping):
            """

            :param arg0:
            :param arg1:
            :param arg2:
            :param args:
            :param kwarg2:
            :param kwargs:"""
            super().__init__(arg0, *args, **kwargs)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_subclass_with_kwargs():
    class BaseClass:
        """description"""

        def __init__(self, arg0, kwarg0=None, kwarg1=None):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None, **kwargs: MutableMapping):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None, **kwargs: MutableMapping):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_subclass_with_args():
    class BaseClass:
        """description"""

        def __init__(self, arg0, kwarg0=None, kwarg1=None):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, *args, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, *args, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_base_with_kwargs():
    class BaseClass:
        """description"""

        def __init__(self, arg0, kwarg0=None, kwarg1=None, **kwargs: MutableMapping):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_base_with_args():
    class BaseClass:
        """description"""

        def __init__(self, arg0, *args, kwarg0=None, kwarg1=None):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, kwarg0=kwarg0)
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_base_with_args_and_mock_empty_dict():
    class BaseClass:
        """description"""

        def __init__(self, arg0, *args, kwarg0=None, kwarg1=None):
            """

            :param arg0:
            :param kwarg0:
            :param kwarg1:"""
            self.arg0 = arg0
            self.kwarg0 = kwarg0
            self.kwarg1 = kwarg1

    class SubClass0(BaseClass):
        """description"""

        @passes_kws_to(BaseClass.__init__)
        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, (), kwarg0=kwarg0, **{})
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    @super_init_pass_on_kws
    class SubClass1(BaseClass):
        """description"""

        def __init__(self, arg0, arg1, arg2, kwarg0=0, kwarg2=None):
            super().__init__(arg0, (), kwarg0=kwarg0, **{})
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg2 = kwarg2

    print(inspect.signature(SubClass0.__init__))
    print(inspect.signature(SubClass1.__init__))

    print(vars(SubClass0(1, 1, 1, kwarg0=52)))
    print(vars(SubClass1(2, 2, 1, kwarg0=52)))


def test_chaining_arbitrary_kwargs():
    def b(c, f, *args, d=None, **kwargs: MutableMapping):
        """description"""
        pass

    def l(im_here=None, **kwargs: MutableMapping):
        """description"""
        pass

    @passes_kws_to(b)
    @passes_kws_to(l)
    def a(e, *args: Sequence, **kwargs: MutableMapping):
        """description"""
        b(1, 2, **kwargs)
        l(**kwargs)

    print(inspect.signature(a))
    a(1, d=None, im_here=2)


def test_chaining_arbitrary_kwargs_keep():
    def b(c, f, *args, d=None, **kwargs: MutableMapping):
        """description"""
        pass

    def l(im_here=None, **kwargs: MutableMapping):
        """description"""
        pass

    @passes_kws_to(b, keep_from_var_kw=True)
    @passes_kws_to(l, keep_from_var_kw=True)
    def a(e, *args: Sequence, **kwargs: MutableMapping):
        """description"""
        b(1, 2, **kwargs)
        l(**kwargs)

    print(inspect.signature(a))
    a(1, d=None, im_here=2)


def test_chaining_no_keep():
    def b(c, f, *args, d: float = None, **kwargs: MutableMapping):
        """description"""
        pass

    def l(a, im_here: str = None, **kwargs: MutableMapping):
        """

        :param a:
        :param im_here: Nice to meet you
        :param kwargs:
        :return:"""
        pass

    @passes_kws_to(b)
    @passes_kws_to(l)
    def a1(e: int, *args: Sequence, **kwargs: MutableMapping):
        """

        :param e:
        :param args:
        :param kwargs:
        :return:"""
        b(1, 2, **kwargs)
        l(1, **kwargs)

    print("a1", inspect.signature(a1))

    @passes_kws_to(b, l)
    def a(e: int, *args: Sequence, **kwargs: MutableMapping):
        """description"""
        pass
        b(1, 2, **kwargs)
        l(1, **kwargs)

    print(inspect.signature(a))
    a(1, d=None, im_here=None)


def test_chaining_no_keep_composed_drop_kws():
    def b(c, f, *args, d: float = None, **kwargs: MutableMapping):
        """description"""
        pass

    def l(a, im_here: str = None, **kwargs: MutableMapping):
        """

        :param a:
        :param im_here: Nice to meet you
        :param kwargs:
        :return:"""
        pass

    @passes_kws_to(b)
    @passes_kws_to(l)
    def a1(e: int, *args: Sequence, **kwargs: MutableMapping):
        """

        :param e:
        :param args:
        :param kwargs:
        :return:"""
        b(1, 2, **kwargs)
        l(1, **kwargs)

    print("a1", inspect.signature(a1))

    @drop_unused_kws
    @passes_kws_to(b, l)
    def a(e: int, *args: Sequence, **kwargs: MutableMapping):
        """description"""
        pass
        b(1, 2, **kwargs)
        l(1, **kwargs)

    print(inspect.signature(a))
    a(1, d=None, im_here=None)
