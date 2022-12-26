import importlib

class Model:

    def __init__(self, mod: str = "", cls: str = None):
        self.__mod = mod
        self.__cls = [cls] if cls else None
        self.__import()

    def __import(self):
        mdl = importlib.import_module(self.__mod)
        if self.__cls is None:
            self.__cls = [c for c in mdl.__dict__ if not c.startswith("_")]
        for name in self.__cls:
            setattr(self, name, getattr(mdl, name))
