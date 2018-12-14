from functools import partial, wraps
from typing import Callable

from warg import NamedOrderedDictionary


def dict_of_func(func: callable = None) -> callable:
  if not func:
    new_debug_func = partial(dict_of_func)
    return new_debug_func

  @wraps(func)
  def wrapper(*args, **kwargs):
    if func.__name__ is not '__init__':
      return NamedOrderedDictionary(func(*args, **kwargs))
    else:
      return func(*args, **kwargs)

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


class NodReturnExampleClass(AutoNodReturns):
  def cool(self):
    return 4

if __name__ == '__main__':

  auto_nod_return = NodReturnExampleClass()

  yes = auto_nod_return.cool()
  assert yes.arg0 == 4
  assert yes.arg0 == yes.as_list()[0]
  print(yes)