from const import *

class LexicalError(Exception):
    def __init__(self, code, lineNumber = None, message = None):
        self.code = code
        self.message = message
        self.lineNumber = lineNumber

    @classmethod
    def withMessage(cls, code, message):
        return cls(code, None, message)

    def __str__(self):
        string = None
        if self.code == INVALID_TOKEN:
            string = "Invalid token"
        else:
            string = "Error {}".format(str(self.code))
        if self.message is not None:
            string += ": {}".format(self.message)
        if self.lineNumber is not None:
            string += " at line {}".format(self.lineNumber)
        return string
