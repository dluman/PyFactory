import inspect
import __main__
import ctypes
import cloudpickle

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
        except:
          # Failing the pickle test, import normal file
          mod = filename.split(".")[0]
          name = mod.replace("/", ".")
          package = name.split(".")[-1]
          module = import_module(name,package = package)
          instance = getattr(module, package)
        return instance
    except:
      raise BadModuleFormatException

  def serialize_as(self, path: str = "", name: str = ""):
    if not name:
        name = self.instance.__name__
    print(self.instance)
    cloudpickle.register_pickle_by_value(self.instance)
    with open(f"{path}{name}", "wb") as fh:
        cloudpickle.dump(self.instance, fh)

  def add_props(self, **kwargs) -> None:
    for arg in kwargs:
      setattr(self.instance, arg, kwargs[arg])

  def add_method(self, method: Callable):
    """ Dynamically add a method to the instance. """
    if callable(method):
        method_name = method.__name__
        bound_method = method.__get__(self.instance, self.instance.__class__)
        setattr(self.instance, method_name, bound_method)
