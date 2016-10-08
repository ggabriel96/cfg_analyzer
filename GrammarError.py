from consts import *

class GrammarError(Exception):
    def __init__(self, code, lineNumber = None, message = None):
        self.code = code
        self.message = message
        self.lineNumber = lineNumber

    # @classmethod
    # def withLine(cls, code, lineNumber):
    #     return cls(cls, code, None, lineNumber)

    def __str__(self):
        string = None
        if self.message is not None:
            string = self.message
        else:
            if self.code == EXPECTED_LT:
                string = "Expected '<' character"
            elif self.code == EMPTY_RULENAME:
                string = "Empty rule name"
            elif self.code == LT_FOBIDDEN:
                string = "'<' character not allowed"
            elif self.code == EXPECTED_COLON:
                string = "Expected ':' caracter"
            elif self.code == EXPECTED_EQUALS:
                string = "Expected '=' character"
            elif self.code == EMPY_PRODUCTION:
                string = "Empty production"
            elif self.code == INVALID_TOKEN:
                string = "Invalid token"
            elif self.code == INVALID_ESCAPE:
                string = "Invalid escape sequence"
            elif self.code == DUPLICATED_RULE:
                string = "Duplicated rule"
            else:
                string = "Error {}".format(str(self.code))
        if self.lineNumber is not None:
            string += " at line {}".format(self.lineNumber)
        return string
