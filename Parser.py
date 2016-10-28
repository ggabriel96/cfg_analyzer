from const import *
from LexicalError import *
from collections import OrderedDict

class Parser():
    def __init__(self, dfa):
        self.dfa = dfa
        self.output = []
        self.symbols = {}
        self.separators = {" ", "(", ")", "*", "/", "%", "^", "?", ":", "<", "=", ">", "[", "]", "{", "}", ".", ",", ";", "'", "\"", "\n"}

    def parse(self, file):
        i = 1
        token_end = 0
        token_start = 0
        current_state = 0
        line = file.readline()
        while line != "":
            print(line)
            for c in line:
                char = ord(c)
                print("char {}: {}".format(c, char))
                token_end += 1
                if c in self.separators:
                    if current_state not in self.dfa.finals and char not in self.dfa.table[current_state]:
                        raise LexicalError(INVALID_TOKEN, i, "'{}'".format(line[token_start:token_end]))
                    if char not in self.dfa.table[current_state]:
                        self.output.append(current_state)
                        current_state = 0
                        token_start = token_end + 1
                        continue
                if char in self.dfa.table[current_state]:
                    current_state = self.dfa.table[current_state][char]
                else:
                    print("'{}' not found on state {}".format(c, current_state))
            i += 1
            line = file.readline()
