import dill
import inspect

from types import MethodType
from typing import Callable
from importlib import import_module
from black import format_str, FileMode

import bypassmappingproxy as bmp

from .Format import Format
from .Errors import BadModuleFormatException

class Form:

  def __init__(self, filename: str = "", *args, **kwargs):
    """ Constructor """
    self.instance = self.__load_module(filename = filename)

  def __load_module(self, filename: str = "", arguments: list = []):
    try:
      with open(filename, "rb") as fh:
        try:
          # Handle as pickle'd file
          instance = dill.load(fh)
        except dill.UnpicklingError:
          # Failing the pickle test, import normal file
          mod = filename.split(".")[0]
          module = import_module(mod)
          instance = getattr(module, mod)
        return instance
    except:
      raise BadModuleFormatException

  def __mainify(self):
    if self.instance.__module__ != "__main__":
      import __main__
      source = inspect.getsource(self.instance)
      co = compile(source, '<string>', 'exec')
      exec(co, __main__.__dict__)

  def make_dillable(self, path: str = "") -> str:
    import __main__
    self.__mainify()
    cls = getattr(__main__, self.instance.__name__)
    for prop in self.instance.__dict__:
      bmp.type_set(cls, prop, self.instance.__dict__[prop])
    self.instance = cls
    with open(f"{path}{self.instance.__name__}", "wb") as fh:
      dill.dump(self.instance, fh)
    return self.instance.__name__

  def add_props(self, **kwargs) -> None:
    for arg in kwargs:
      setattr(self.instance, arg, kwargs[arg])

  def add_method(self, method: Callable = ()) -> None:
    setattr(self.instance, method.__name__, MethodType(method, self.instance))
