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
        # Create copy of the object at the address of the instance
        ptr = ctypes.cast(id(self.instance), ctypes.py_object)

        # Change the __module__ to '__main__'
        ptr.value.__module__ = "__main__"

        # Optionally, copy the class definition to __main__ if not already there
        class_name = ptr.value.__name__
        if class_name not in __main__.__dict__:
            # Set the mainify'd version to the object created at the pointer
            __main__.__dict__[class_name] = ptr.value

        # Return the full object context stored at the location of the pointer
        return ptr.value

  def make_dillable(self, path: str = "") -> str:
    ptr = self.__mainify()
    cls = __main__.__dict__[ptr.__name__]

    # TODO: The two objects are the same now, but trigger a recursion error

    with open(f"{path}{ptr.__name__}", "wb") as fh:
      dill.dump(cls, fh)
    return ptr.__name__

  def add_props(self, **kwargs) -> None:
    for arg in kwargs:
      setattr(self.instance, arg, kwargs[arg])

  def add_method(self, method: Callable = ()) -> None:
    if callable(method):
      setattr(self.instance, method.__name__, MethodType(method, self.instance))
