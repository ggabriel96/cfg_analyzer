class Symbol():
    def __init__(self, name, isterm):
        self.name = name
        self.isterm = isterm

    def __str__(self):
        if self.isterm:
            if self.name == "":
                return "&"
            return "'{}'".format(self.name)
        return "<{}>".format(self.name)
