class ItemCopy(Exception):

    copy = True

    def __init__(self):
        pass

    def __str__(self):
        return f"Copy status: {self.copy}"

