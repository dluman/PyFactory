# springform

[![PyPI version](https://img.shields.io/pypi/v/springform)](https://pypi.org/project/springform/)

An simple templating system for Python class files.

## Installation

Find this tool on `PyPI`: `pip install springform`

## Usage

Given the following template file (let's call it `Item.py`):

```python
from time import sleep

class Item(object):

    copy = False

    def __init__(self):
        pass

    def __str__(self):
        return f"Copy status: {self.copy}"
```

and a reasonable driver (aw heck, let's call it `main.py`):

```python
from springform import Form

def __dumb(self):
    print("It really is.")

def main():
    template = Form(mod = "Item", cls = "Item")
    template.make("ItemCopy", copy = True, __dumb = __dumb)

if __name__ == "__main__":
    main()
```

The module should make a new file in the current working directory: `ItemCopy.py`
whose `__str__` magic will report to you that it's a _copy_ (the above example changes
the value of the `copy` instance variable).

## Notes

The module can handle single or multiple inheritance as of `0.2.0` -- find it everywhere
reputable Python modules are listed (i.e. only `PyPI`, rly).

Obligatory "it's under construction" statement.
