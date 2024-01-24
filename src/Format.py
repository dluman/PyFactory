import re
import dill
import inspect
import autopep8

from black import format_str, FileMode

class Format:

  @staticmethod
  def prepare_function(function_code: str = "", depth: int = 1) -> str:
    lines = function_code.split("\n")
    for line in range(len(lines)):
      lines[line] = re.sub("\n\s+"," ",lines[line])
      lines[line] = f"\t{lines[line]}"
    return "\n".join(lines)

  @staticmethod
  def compile_changes(instance) -> str:
    changes = ""
    for change in instance.__dict__:
      kind = type(instance.__dict__[change])
      if inspect.ismethod(getattr(instance,change)):
        changes += change
    return changes

  @staticmethod
  def code_to_string(instance) -> str:
    return dill.source.getsource(instance.__class__)

  @staticmethod
  def tabs_to_spaces(instance) -> str:
    return autopep8.fix_code(
      Format.code_to_string(instance) + Format.compile_changes(instance)
    )
    #return format_str(
    #  Format.code_to_string(instance) + Format.compile_changes(instance),
    #  mode = FileMode()
    #)
