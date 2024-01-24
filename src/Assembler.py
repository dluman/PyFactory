import inspect

from types import Callable

class Assembler:

  EXCLUDES = [
    "__doc__",
    "__weakref__"
  ]

  # TODO: Develop a way to get inherited classes, because it matters.

  def __init__(self, members: dict = {}):
    self.members = {elem: members[elem] for elem in members if elem not in excludes}
    self.__assemble()

  def __make_callable(self, callable: Callable()) -> str:
    return (f"\t{inspect.getsource(callable)}")

  def __assemble(self):
    excludes = ["__doc__", "__weakref__"]
    for elem in self.members:
      if callable(elem) and not inspect.isclass(elem):
        self.__make_callable(elem)
