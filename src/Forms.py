import dill

from types import MethodType
from typing import Callable
from importlib import import_module

class Form:

  def __init__(self, filename: str = "", *args, **kwargs):
    self.instance = self.__load_module(
      filename = filename
      #arguments =  self.__concat_args(args, kwargs)
    )()

  def __open_file(self, filename: str = "") -> bytes:
    try:
      with open(filename, "rb") as fh:
        data = fh.read()
        return data
    except:
      print("File open error.")
      exit()

  def __concat_args(self, *args, **kwargs) -> dict:
    arguments = [args]
    arguments.append(kwargs)
    return arguments

  def __load_module(self, filename: str = "", arguments: list = []):
    try:
      mod = filename.split(".")[0]
      module = import_module(mod)
      instance = getattr(module, mod)
      return instance
    except:
      print("It appears that the module was called incorrectly.")
      exit()

  def __set_template_name(self, filename: str = "") -> str:
    return ".".join(filename.split(".")[:-1])

  def add_method(self, method: Callable = ()) -> None:
    setattr(self.instance, method.__name__, MethodType(method, self.instance))

  def convert(self, filename: str = "", *args, **kwargs) -> bool:
    instance = self.__load_module(filename)
    template_name = f"{self.__set_template_name(filename)}.form"
    with open(template_name, "wb") as fh:
      dill.dump(instance(), fh)
    return True
