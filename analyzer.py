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
EXPECTED_LT = -1
EMPTY_RULENAME = -2
LT_FOBIDDEN = -3
EXPECTED_COLON = -4
EXPECTED_EQUALS = -5
EMPY_PRODUCTION = -6
INVALID_TOKEN = -7
INVALID_ESCAPE = -8

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
            else:
                string = "Error {}".format(str(self.code))
        if self.lineNumber is not None:
            string += " at line {}".format(self.lineNumber)
        return string

class Symbol():
    def __init__(self, name, isterm):
        self.name = name
        self.isterm = isterm

class Analyzer():
    def read_grammar(self, grammarFile):
        i = 1;
        state = SEEK_RULE
        line = grammarFile.readline()
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
                        raise GrammarError(EXPECTED_LT, i)
                elif state == SEEK_RULE_NAME:
                    if c == '>':
                        if rulename != "":
                            print("\nRead rule: '{}'".format(rulename))
                            state = SEEK_ST_COLON
                        else:
                            raise GrammarError(EMPTY_RULENAME, i)
                    elif c == '<':
                        raise GrammarError(LT_FOBIDDEN, i)
                    else:
                        rulename += c
                elif state == SEEK_ST_COLON:
                    if c == ' ':
                        continue
                    if c == ':':
                        state = SEEK_ND_COLON
                    else:
                        raise GrammarError(EXPECTED_COLON, i)
                elif state == SEEK_ND_COLON:
                    if c == ':':
                        state = SEEK_EQUALS
                    else:
                        raise GrammarError(EXPECTED_COLON, i)
                elif state == SEEK_EQUALS:
                    if c == '=':
                        state = SEEK_ST_PROD;
                    else:
                        raise GrammarError(EXPECTED_EQUALS, i)
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
                        raise GrammarError(EMPY_PRODUCTION, i)
                    else:
                        raise GrammarError(INVALID_TOKEN, i)
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
                        raise GrammarError(LT_FOBIDDEN, i)
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
                        raise GrammarError(INVALID_ESCAPE, i)
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
                        raise GrammarError(INVALID_TOKEN, i)
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
                        raise GrammarError(LT_FOBIDDEN, i)
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
                        raise GrammarError(INVALID_ESCAPE, i)
                else:
                    raise RuntimeError("Reached invalid state {}".format(state))
            i += 1
            line = grammarFile.readline()
