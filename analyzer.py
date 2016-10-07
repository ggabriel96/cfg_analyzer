#!/bin/python3.5

separators = {" ", "(", ")", "+", "-", "*", "/", "%", "^", "?", ":", "<", "=", ">", "[", "]", "{", "}", ".", ",", ";", "'", "\""}

SEEK_RULE = 1
SEEK_RULE_NAME = 2
SEEK_ST_COLON = 3
SEEK_ND_COLON = 4
SEEK_EQUALS = 5
SEEK_ST_PROD = 6
SEEK_ST_TERM = 7
SEEK_ST_NTERM = 8
SEEK_ST_ESC = 9
SEEK_PROD = 10
SEEK_TERM = 11
SEEK_NTERM = 12
SEEK_ESC = 13

class GrammarError(Exception):
    EXPECTED_LT = -1
    EMPTY_RULENAME = -2
    LT_FOBIDDEN = -3
    EXPECTED_COLON = -4
    EXPECTED_EQUALS = -5
    EMPY_PRODUCTION = -6
    INVALID_TOKEN = -7
    INVALID_ESCAPE = -8

    def __init__(self, code, message = None, lineNumber = None):
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
        if self.lineNumber is not None:
            if string is not None:
                string += ", at line {}".format(self.lineNumber)
            else:
                string = "at line {}".format(self.lineNumber)
        if string is not None:
            string += ", "
        else:
            string = str()
        if self.code == GrammarError.EXPECTED_LT:
            string += "EXPECTED_LT"
        elif self.code == GrammarError.EMPTY_RULENAME:
            string += "EMPTY_RULENAME"
        elif self.code == GrammarError.LT_FOBIDDEN:
            string += "LT_FOBIDDEN"
        elif self.code == GrammarError.EXPECTED_COLON:
            string += "EXPECTED_COLON"
        elif self.code == GrammarError.EXPECTED_EQUALS:
            string += "EXPECTED_EQUALS"
        elif self.code == GrammarError.EMPY_PRODUCTION:
            string += "EMPY_PRODUCTION"
        elif self.code == GrammarError.INVALID_TOKEN:
            string += "INVALID_TOKEN"
        elif self.code == GrammarError.INVALID_ESCAPE:
            string += "INVALID_ESCAPE"
        else:
            string = "error {}".format(str(self.code))
        return string

class Symbol():
    def __init__(self, name, isterm):
        self.name = name
        self.isterm = isterm

def read_grammar(f):
    i = 1;
    state = SEEK_RULE
    line = f.readline()
    while (line != ""):
        term = None
        nterm = None
        rulename = str()
        for c in line:
            if state == SEEK_RULE:
                if c == ' ':
                    continue
                if c == '<':
                    state = SEEK_RULE_NAME
                elif c == '*':
                    print("\nSpecial rule");
                else:
                    raise GrammarError(GrammarError.EXPECTED_LT)
            elif state == SEEK_RULE_NAME:
                if c == '>':
                    if rulename != "":
                        print("\nRead rule: '{}'".format(rulename))
                        state = SEEK_ST_COLON
                    else:
                        raise GrammarError(GrammarError.EMPTY_RULENAME)
                elif c == '<':
                    raise GrammarError(GrammarError.LT_FOBIDDEN)
                else:
                    rulename += c
            elif state == SEEK_ST_COLON:
                if c == ' ':
                    continue
                if c == ':':
                    state = SEEK_ND_COLON
                else:
                    raise GrammarError(GrammarError.EXPECTED_COLON)
            elif state == SEEK_ND_COLON:
                if c == ':':
                    state = SEEK_EQUALS
                else:
                    raise GrammarError(GrammarError.EXPECTED_COLON)
            elif state == SEEK_EQUALS:
                if c == '=':
                    state = SEEK_ST_PROD;
                else:
                    raise GrammarError(GrammarError.EXPECTED_EQUALS)
            elif state == SEEK_ST_PROD:
                if c == ' ':
                    continue
                if c == '"':
                    term = str()
                    state = SEEK_ST_TERM
                elif c == '<':
                    nterm = str()
                    state = SEEK_ST_NTERM
                elif c == '\n':
                    raise GrammarError(GrammarError.EMPY_PRODUCTION)
                else:
                    raise GrammarError(GrammarError.INVALID_TOKEN)
            elif state == SEEK_ST_TERM:
                if c == '\\':
                    state = SEEK_ST_ESC
                elif c == '"':
                    print("Read terminal: '{}'".format(term))
                    state = SEEK_PROD
                else:
                    term += c
            elif state == SEEK_ST_NTERM:
                if c == '<':
                    raise GrammarError(GrammarError.LT_FOBIDDEN)
                elif c == '>':
                    print("Read nonterminal: '{}'".format(nterm))
                    state = SEEK_PROD
                else:
                    nterm += c
            elif state == SEEK_ST_ESC:
                if c == '"' or c == '\\':
                    term += c
                    state = SEEK_ST_TERM
                else:
                    raise GrammarError(GrammarError.INVALID_ESCAPE)
            elif state == SEEK_PROD:
                if c == ' ':
                    continue
                if c == '"':
                    term = str()
                    state = SEEK_TERM
                elif c == '<':
                    nterm = str()
                    state = SEEK_NTERM
                elif c == '|':
                    print("End of production")
                    state = SEEK_ST_PROD
                elif c == '\n':
                    state = SEEK_RULE
                else:
                    raise GrammarError(GrammarError.INVALID_TOKEN)
            elif state == SEEK_TERM:
                if c == '\\':
                    state = SEEK_ESC
                elif c == '"':
                    print("Read terminal: '{}'".format(term))
                    state = SEEK_PROD
                else:
                    term += c
            elif state == SEEK_NTERM:
                if c == '<':
                    raise GrammarError(GrammarError.LT_FOBIDDEN)
                elif c == '>':
                    print("Read nonterminal: '{}'".format(nterm))
                    state = SEEK_PROD
                else:
                    nterm += c
            elif state == SEEK_ESC:
                if c == '"' or c == '\\':
                    term += c
                    state = SEEK_TERM
                else:
                    raise GrammarError(GrammarError.INVALID_ESCAPE)
            else:
                raise RuntimeError("Reached invalid state {}".format(state))
        i += 1
        line = f.readline()
