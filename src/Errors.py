class BadModuleFormatException(Exception):

  def __init__(self, filename: str = "", *args):
    super().__init__(args)
    print("Incorrect module format: not a Python file or Pickle.")
