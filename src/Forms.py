import inspect
import importlib

from .Model import Model

class Form:

    @staticmethod
    def __isdunder(name: str = "") -> bool:
        """ Tests if a variable is a dunder """
        return name.startswith("__")

    def __init__(self, mod: str = "", cls: str = ""):
        """ Constructor """
        self.__mod = mod
        self.__cls = cls
        self.template = Model(
            mod = self.__mod,
            cls = self.__cls
        )
        self.__elements = {
            "impt": {},
            "bases": {},
            "func": {},
            "vars": {}
        }
        self.__imported()
        self.__inherit()
        self.__assemble()

    def __imported(self) -> list:
        """ Retrieves list of extant imports """
        imports = {}
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
                imports[name] = {"from": parent}
        self.__elements["impt"] = imports

    def __update(self, members: list = [()]) -> None:
        """ Updates code member values """
        # TODO: Write in a "membership" for ast writing later?
        for member in members:
            name, value = member
            if inspect.isfunction(value):
                src = inspect.getsource(value)
                self.__elements["func"][name] = src
            elif not self.__isdunder(name):
                try:
                    value.__objclass__
                    continue
                except AttributeError: pass
                self.__elements["vars"][name] = value

    def __inherit(self) -> None:
        """ Processes inherited classes """
        bases = []
        if self.__cls:
            # TODO: Find a better way to get this information with libCST or ast
            mdl = eval(f"importlib.import_module('{self.__mod}').{self.__cls}")
            for base in mdl.__bases__:
                bases.append(base.__name__)
        self.__elements["bases"] = bases

    def __assemble(self) -> None:
        """ Assembles all of the preprocessed parts """
        members = inspect.getmembers(
            getattr(self.template, self.__mod)
        )
        self.__update(members)

    def remove(self, removal: str = "") -> None:
        for category in self.__elements:
            elements = self.__elements[category]
            if removal in elements:
                if type(elements) == list:
                    elements.remove(removal)
                if type(elements) == dict:
                    del elements[removal]

    def make(self, name: str = "", imports: dict = {}, **kwargs) -> None:
        # TODO: Rewrite with ast pronto
        """A sorry mess."""
        lines = []
        # Update members with provided kwargs
        self.__update(
            list(kwargs.items())
        )
        # Establish new imports/dependencies
        for lib in self.__elements["impt"]:
            stmt = ""
            mod = self.__elements["impt"][lib]
            if mod["from"]: stmt = f"from {mod['from']} "
            stmt += f"import {lib}"
            lines.append(f"{stmt}")
        lines.append("")
        # Create class declaration
        lines.append(f"class {name}({','.join(self.__elements['bases'])}):\n")
        # Create global variables
        for var in self.__elements["vars"]:
            val = self.__elements["vars"][var]
            lines.append(f"{' '*4}{var} = {val}")
        lines.append("")
        # Provide methods/functions
        for func in self.__elements["func"]:
            code = self.__elements["func"][func]
            if not code.startswith(" "):
                code = f"{' ' * 4}{code.replace(' ' * 4,' ' * 8)}"
            lines.append(code)
        # Write file
        with open(f"{name}.py", "w") as fh:
            for line in lines:
                fh.write(line + "\n")
