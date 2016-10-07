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
ERR_LESS = -1
ERR_EMPTY_RULE = -2
ERR_LESS_FORBID = -3
ERR_COLON = -4
ERR_EQUALS = -5
ERR_EMPTY = -6
ERR_TOK = -7
ERR_ESC = -8

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
                    raise SyntaxError(ERR_LESS)
            elif state == SEEK_RULE_NAME:
                if c == '>':
                    if rulename != "":
                        print("\nRead rule: '{}'".format(rulename))
                        state = SEEK_ST_COLON
                    else:
                        raise SyntaxError(ERR_EMPTY_RULE)
                elif c == '<':
                    raise SyntaxError(ERR_LESS_FORBID)
                else:
                    rulename += c
            elif state == SEEK_ST_COLON:
                if c == ' ':
                    continue
                if c == ':':
                    state = SEEK_ND_COLON
                else:
                    raise SyntaxError(ERR_COLON)
            elif state == SEEK_ND_COLON:
                if c == ':':
                    state = SEEK_EQUALS
                else:
                    raise SyntaxError(ERR_COLON)
            elif state == SEEK_EQUALS:
                if c == '=':
                    state = SEEK_ST_PROD;
                else:
                    raise SyntaxError(ERR_EQUALS)
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
                    raise SyntaxError(ERR_EMPTY)
                else:
                    raise SyntaxError(ERR_TOK)
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
                    raise SyntaxError(ERR_LESS_FORBID)
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
                    raise SyntaxError(ERR_ESC)
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
                    raise SyntaxError(ERR_TOK)
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
                    raise SyntaxError(ERR_LESS_FORBID)
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
                    raise SyntaxError(ERR_ESC)
            else:
                raise RuntimeError("Reached invalid state {}".format(state))
        i += 1
        line = f.readline()
