from const import *
from Symbol import *
from GrammarError import *

class Grammar():
    def __init__(self, verbose = False):
        # https://docs.python.org/3/library/stdtypes.html#dict
        self.rules = {}
        # https://docs.python.org/3/library/stdtypes.html#set
        self.asterisk = set()
        self.ignore = set()
        self.finals = set()
        self.verbose = verbose

    def readgr(self, grammarFile):
        i = 1
        state = SEEK_RULE
        line = grammarFile.readline()
        while (line != ""):
            symbol = None
            special = False
            ignore = False
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
                    elif c == '+':
                        ignore = True
                    else:
                        raise GrammarError(EXPECTED_LT, i)
                elif state == SEEK_RULE_NAME:
                    if c == '>':
                        if rulename != "":
                            if rulename in self.rules:
                                raise GrammarError(DUPLICATED_RULE, i)
                            if special:
                                self.asterisk.add(rulename)
                            elif ignore:
                                self.ignore.add(rulename)
                            self.rules[rulename] = list()
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
                        self.rules[rulename].append(production)
                        production = list()
                        state = SEEK_ST_PROD

                        if self.verbose:
                            print("End of production")
                    elif c == '\n':
                        self.rules[rulename].append(production)
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
        for rule, productions in self.rules.items():
            print("<{}> ::= ".format(rule), end = "")
            for production in productions:
                for symbol in production:
                    print(symbol, end = "")
                print(" | ", end = "")
            print()
