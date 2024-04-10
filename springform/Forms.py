import dill
import inspect
import __main__
import ctypes

from types import MethodType, ModuleType
from typing import Callable
from importlib import import_module

import bypassmappingproxy as bmp

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
          name = mod.replace("/", ".")
          package = name.split(".")[-1]
          module = import_module(name,package = package)
          instance = getattr(module, package)
        return instance
    except:
      raise BadModuleFormatException

  def __mainify(self):
    if self.instance.__module__ != "__main__":
      # Below only grabs the original code
      #source = inspect.getsource(self.instance)
      setattr(self.instance,"__module__","")
      source = inspect.getsource(ctypes.cast(id(self.instance), ctypes.py_object).value)
      co = compile(source, '<string>', 'exec')
      exec(co, __main__.__dict__)
      for prop in self.instance.__dict__:
        bmp.type_set(__main__.__dict__[self.instance.__name__], prop, self.instance.__dict__[prop])

  def make_dillable(self, path: str = "") -> str:
    self.__mainify()
    cls = getattr(__main__, self.instance.__name__)
    print(self.instance.__dict__)
    with open(f"{path}{self.instance.__name__}", "wb") as fh:
      dill.dump(cls, fh)
    return self.instance.__name__

  def add_props(self, **kwargs) -> None:
    for arg in kwargs:
      setattr(self.instance, arg, kwargs[arg])

  def add_method(self, method: Callable = ()) -> None:
    if callable(method):
      setattr(self.instance, method.__name__, MethodType(method, self.instance))
