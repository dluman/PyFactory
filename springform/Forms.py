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
          """ Modify the instance's class __module__ attribute to '__main__' and ensure the class is copied to __main__. """
          cls = self.instance.__class__
          class_name = cls.__name__
          
          # Get a pointer to the class object and change its __module__
          ptr = ctypes.cast(id(cls), ctypes.py_object)
          ptr.value.__module__ = "__main__"
          
          # If the class is not in __main__, create a shallow copy in __main__
          if class_name not in __main__.__dict__:
              new_class = type(class_name, cls.__bases__, {k: v for k, v in cls.__dict__.items() if not k.startswith('__')})
              __main__.__dict__[class_name] = new_class
              self.instance.__class__ = new_class
          else:
              self.instance.__class__ = __main__.__dict__[class_name]
        
      # def __mainify(self):
      #   """ Modify the instance's class to ensure it is defined in __main__ module. """
      #   cls = self.instance.__class__
      #   class_name = cls.__name__
        
      #   if cls.__module__ != "__main__":
      #       # Check if the class is already defined in __main__
      #       if class_name not in __main__.__dict__:
      #           # Prepare new class attributes excluding problematic ones
      #           new_class_dict = {}
      #           for key, value in cls.__dict__.items():
      #               if isinstance(value, (staticmethod, classmethod)):
      #                   # Copy static and class methods as is
      #                   new_class_dict[key] = value
      #               elif isinstance(value, FunctionType):
      #                   # Convert functions to unbound methods
      #                   new_class_dict[key] = value
      #               elif isinstance(value, property):
      #                   # Ensure properties are transferred correctly
      #                   new_class_dict[key] = value
      #               elif not key.startswith('__'):
      #                   # Regular attributes that do not start with __
      #                   new_class_dict[key] = value

      #           # Create a new class type manually setting __module__ and __qualname__
      #           new_class = type(class_name, cls.__bases__, new_class_dict)
      #           new_class.__module__ = "__main__"
      #           new_class.__qualname__ = class_name

      #           # Assign the new class to the __main__ module dictionary
      #           __main__.__dict__[class_name] = new_class

      #       # Update the instance's class reference to the new class or existing class in __main__
      #       self.instance.__class__ = __main__.__dict__[class_name]
        
      #   # Use ctypes to modify the __module__ of the original class directly if needed
      #   # This step is risky and should be done with understanding the consequences
      #   ptr = ctypes.cast(id(cls), ctypes.py_object)
      #   try:
      #       ptr.value.__module__ = "__main__"
      #   except TypeError as e:
      #       print(f"Failed to change __module__ with ctypes due to: {e}")
            
  def make_dillable(self, path: str = "") -> str:
    self.__mainify()
    filename = f"{path}{self.instance.__class__.__name__}.pkl"
    with open(filename, "wb") as fh:
      dill.dump(self.instance, fh)
    return filename

  def add_props(self, **kwargs) -> None:
    for arg in kwargs:
      setattr(self.instance, arg, kwargs[arg])

  
  def add_method(self, method: Callable):
    """ Dynamically add a method to the instance. """
    if callable(method):
        method_name = method.__name__
        bound_method = method.__get__(self.instance, self.instance.__class__)
        setattr(self.instance, method_name, bound_method)

  # def add_method(self, method: Callable = ()) -> None:
  #   if callable(method):
  #     setattr(self.instance, method.__name__, MethodType(method, self.instance))
