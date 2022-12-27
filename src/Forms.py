import inspect
import importlib

from .Model import Model

class Form:

    @staticmethod
    def __isdunder(name: str = "") -> bool:
        return name.startswith("__")

    def __init__(self, mod: str = "", cls: str = ""):
        self.__mod = mod
        self.__cls = cls
        self.template = Model(
            mod = self.__mod,
            cls = self.__cls
        )
        self.__elements = {
            "func": {},
            "vars": {}
        }
        self.__imports = self.__imported()
        self.__bases = self.__inherit()
        self.__assemble()

    def __imported(self) -> list:
        imports = []
        mod = importlib.import_module(self.__mod)
        members = inspect.getmembers(mod)
        for member in members:
            parent = None
            name, value = member
            if inspect.ismodule(value) or inspect.isbuiltin(value):
                try:
                    parent = value.__module__
                except AttributeError:
                    pass
                imports.append({
                    "from": parent,
                    "import": name
                })
        return imports

    def __inherit(self) -> str:
        bases = []
        if self.__cls:
            mdl = eval(f"importlib.import_module('{self.__mod}').{self.__cls}")
            for base in mdl.__bases__:
                bases.append(base.__name__)
        if bases:
            return f"({','.join(name for name in bases)})"
        return ""

    def __assemble(self) -> None:
        members = getattr(self.template, self.__mod)
        for member in inspect.getmembers(members):
            name, value = member
            if inspect.isfunction(value):
                src = inspect.getsource(value)
                self.__elements["func"][name] = src
            elif not self.__isdunder(name):
                try:
                    value.__objclass__
                    continue
                except AttributeError:
                    pass
                self.__elements["vars"][name] = value

    def make(self, name: str = "", **kwargs) -> None:
        lines = []
        for kwarg in kwargs:
            val = kwargs[kwarg]
            # TODO: Organize this and the similar call
            #       above -- you do too much work
            if inspect.isfunction(val):
                self.__elements["func"][kwarg] = inspect.getsource(val)
            else:
               self.__elements["vars"][kwarg] = val
        for imported in self.__imports:
            stmt = ""
            if imported["from"]: stmt = f"from {imported['from']} "
            stmt += f"import {imported['import']}"
            lines.append(f"{stmt}")
        lines.append("")
        lines.append(f"class {name}{self.__bases}:\n")
        for var in self.__elements["vars"]:
            val = self.__elements["vars"][var]
            lines.append(f"{' '*4}{var} = {val}")
        lines.append("")
        for func in self.__elements["func"]:
            code = self.__elements["func"][func]
            if not code.startswith(" "):
                code = f"{' ' * 4}{code.replace(' ' * 4,' ' * 8)}"
            lines.append(code)
        with open(f"{name}.py", "w") as fh:
            for line in lines:
                fh.write(line + "\n")
