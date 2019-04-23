from functools import partial, wraps
from inspect import signature
from typing import Callable, Iterable, Mapping

from sorcery import dict_of

from warg import NamedOrderedDictionary


def dict_of_func(func: callable = None) -> callable:
    if not func:
        new_debug_func = partial(dict_of_func)
        return new_debug_func

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__ is not "__init__":
            return_value = func(*args, **kwargs)
            if isinstance(return_value, NamedOrderedDictionary):
                return return_value
            elif isinstance(return_value, Mapping):
                return NamedOrderedDictionary(**return_value)
            elif isinstance(return_value, Iterable):
                return NamedOrderedDictionary(*return_value)
            return NamedOrderedDictionary(return_value)
        else:
            return func(*args, **kwargs)

    sig = signature(func)
    sig = sig.replace(return_annotation=NamedOrderedDictionary)
    func.__signature__ = sig
    wrapper.__signature__ = sig

    return wrapper


def nod_return_class(cls):
    for [method_key, method_value] in vars(cls).items():
        if isinstance(method_value, Callable):
            setattr(cls, method_key, dict_of_func(method_value))
    return cls


class MetaNodReturnBase(type):
    def __new__(cls, *args, **kwargs):
        class_obj = super().__new__(cls, *args, **kwargs)
        class_obj = nod_return_class(class_obj)
        return class_obj


class AutoNodReturns(metaclass=MetaNodReturnBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":

    class NodReturnExampleClass(AutoNodReturns):
        def cool(self, agkjas):
            slfs = 4 + agkjas
            return NamedOrderedDictionary(4, **dict_of(slfs))

        def hot(self):
            s = 7
            a = 2
            return dict_of(s, a)

        def luke_warm(self, a, b):
            return 1, 3, 5

    auto_nod_return = NodReturnExampleClass()

    yes = auto_nod_return.cool(5)
    print(yes)
    assert yes.arg0 == 4
    assert yes.arg0 == yes.as_list()[0]

    no = auto_nod_return.hot()
    print(no)
    assert no.a == 2
    assert no.s == 7

    maybe = auto_nod_return.luke_warm(2, 8)
    print(maybe)
    assert maybe.arg1 == 3
    assert maybe.arg2 == 5
