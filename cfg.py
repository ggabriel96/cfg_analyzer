#!/bin/python3.5
import sys

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
DUPLICATED_RULE = -9

separators = {" ", "(", ")", "+", "-", "*", "/", "%", "^", "?", ":", "<", "=", ">", "[", "]", "{", "}", ".", ",", ";", "'", "\""}

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

class Analyzer():
    def __init__(self, verbose = False):
        # https://docs.python.org/3/library/stdtypes.html#dict
        self.grammar = {}
        # https://docs.python.org/3/library/stdtypes.html#set
        self.asterisk = set()
        self.finals = set()
        self.verbose = verbose

    def readgr(self, grammarFile):
        i = 1
        state = SEEK_RULE
        line = grammarFile.readline()
        while (line != ""):
            symbol = None
            special = False
            rulename = str()
            production = None
            for c in line:
                if state == SEEK_RULE:
                    if c == ' ':
                        continue
                    if c == '<':
                        state = SEEK_RULE_NAME
                    elif c == '*':
                        special = True
                    else:
                        raise GrammarError(EXPECTED_LT, i)
                elif state == SEEK_RULE_NAME:
                    if c == '>':
                        if rulename != "":
                            if rulename in self.grammar:
                                raise GrammarError(DUPLICATED_RULE, i)
                            if special:
                                self.asterisk.add(rulename)
                            self.grammar[rulename] = list()
                            state = SEEK_ST_COLON

                            if self.verbose:
                                print("\nRule '{}'".format(rulename))
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
                        production = list()
                        state = SEEK_ST_PROD;
                    else:
                        raise GrammarError(EXPECTED_EQUALS, i)
                elif state == SEEK_ST_PROD:
                    if c == ' ':
                        continue
                    if c == '"':
                        symbol = str()
                        state = SEEK_ST_TERM
                    elif c == '<':
                        symbol = str()
                        state = SEEK_ST_NTERM
                    elif c == '\n':
                        raise GrammarError(EMPY_PRODUCTION, i)
                    else:
                        raise GrammarError(INVALID_TOKEN, i)
                elif state == SEEK_ST_TERM:
                    if c == '\\':
                        state = SEEK_ST_ESC
                    elif c == '"':
                        production.append(Symbol(symbol, True))
                        state = SEEK_PROD

                        if self.verbose:
                            print("Terminal '{}'".format(symbol))
                    else:
                        symbol += c
                elif state == SEEK_ST_NTERM:
                    if c == '<':
                        raise GrammarError(LT_FOBIDDEN, i)
                    elif c == '>':
                        production.append(Symbol(symbol, False))
                        state = SEEK_PROD

                        if self.verbose:
                            print("Non-terminal '{}'".format(symbol))
                    else:
                        symbol += c
                elif state == SEEK_ST_ESC:
                    if c == '"' or c == '\\':
                        symbol += c
                        state = SEEK_ST_TERM
                    else:
                        raise GrammarError(INVALID_ESCAPE, i)
                elif state == SEEK_PROD:
                    if c == ' ':
                        continue
                    if c == '"':
                        symbol = str()
                        state = SEEK_TERM
                    elif c == '<':
                        symbol = str()
                        state = SEEK_NTERM
                    elif c == '|':
                        self.grammar[rulename].append(production)
                        production = list()
                        state = SEEK_ST_PROD

                        if self.verbose:
                            print("End of production")
                    elif c == '\n':
                        self.grammar[rulename].append(production)
                        state = SEEK_RULE

                        if self.verbose:
                            print("End of rule")
                    else:
                        raise GrammarError(INVALID_TOKEN, i)
                elif state == SEEK_TERM:
                    if c == '\\':
                        state = SEEK_ESC
                    elif c == '"':
                        production.append(Symbol(symbol, True))
                        state = SEEK_PROD

                        if self.verbose:
                            print("Terminal '{}'".format(symbol))
                    else:
                        symbol += c
                elif state == SEEK_NTERM:
                    if c == '<':
                        raise GrammarError(LT_FOBIDDEN, i)
                    elif c == '>':
                        production.append(Symbol(symbol, False))
                        state = SEEK_PROD

                        if self.verbose:
                            print("Non-terminal '{}'".format(symbol))
                    else:
                        symbol += c
                elif state == SEEK_ESC:
                    if c == '"' or c == '\\':
                        symbol += c
                        state = SEEK_TERM
                    else:
                        raise GrammarError(INVALID_ESCAPE, i)
                else:
                    raise RuntimeError("Reached invalid state {}".format(state))
            i += 1
            line = grammarFile.readline()

    def printgr(self):
        for rule, productions in self.grammar.items():
            print("<{}> ::= ".format(rule), end = "")
            for production in productions:
                for symbol in production:
                    print(symbol, end = "")
                print(" | ", end = "")
            print()

def main(argv):
    # The with statement allows objects like files to be used in a way
    # that ensures they are always cleaned up promptly and correctly.
    with open(argv[1], 'r') as f:
        a = Analyzer()
        a.readgr(f)
        print("Special states:")
        print(a.asterisk)
        print("\nGrammar:")
        a.printgr()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv);
