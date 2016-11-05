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
        current_state = 0
        line = file.readline()
        while line != "":
            print("-------------------------------------\nline: {}".format(line))
            caret = 0
            token_start = 0
            readSeparator = False
            while caret < len(line):
                char = line[caret]
                # spaces just matter inside strings, so it's
                # safe to ignore them while in initial state
                if current_state == 0 and (char == ' ' or char == '\n') :
                    caret += 1
                    token_start = caret
                    continue
                c = ord(char)
                print("\n({}, '{}')".format(current_state, char if char != '\n' else "\\n"))
                if char in self.separators:
                    print("'{}' is a separator".format(char if char != '\n' else "\\n"))
                    # if we're not at a final state and there is no mapping for
                    # this char in the current state, then we found an error
                    if current_state not in self.dfa.finals and c not in self.dfa.table[current_state]:
                        raise LexicalError(INVALID_TOKEN, i, "'{}'".format(line[token_start:caret]))
                    # but if we're at a final state and still there's no mapping
                    # we simply reached a final state of a separator
                    if c not in self.dfa.table[current_state]:
                        self.output.append(str(current_state) + ": '" + line[token_start:caret] + "'")
                        print("self.output: {}".format(self.output))
                        token_start = caret
                        print("Resetting...")
                        current_state = 0
                        if char == '\n':
                            caret += 1
                        continue
                    if current_state == 0 or readSeparator:
                        print("Initial state or readSeparator is True: ({}, '{}') -> {}".format(current_state, char, self.dfa.table[current_state][c]))
                        current_state = self.dfa.table[current_state][c]
                        # readSeparator was not necessarily True to enter
                        # this if and we might later need it True here
                        readSeparator = True
                        caret += 1
                        continue
                # if we're not looking at a separator and there's a mapping for it in the current state...
                if c in self.dfa.table[current_state]:
                    print("({}, '{}') -> {}".format(current_state, char, self.dfa.table[current_state][c]))
                    current_state = self.dfa.table[current_state][c]
                # if we previously looked at a separator and it just reached
                # its final state here, right in the face of an ordinary character
                elif readSeparator and c in self.dfa.table[0]:
                    print("Previously read a separator and there's a mapping in the initial state")
                    self.output.append(str(current_state) + ": '" + line[token_start:caret] + "'")
                    current_state = self.dfa.table[0][c]
                    token_start = caret
                else:
                    raise LexicalError(INVALID_TOKEN, i, "'{}' not mapped on state {}".format(char, current_state))
                readSeparator = False
                print("self.output: {}".format(self.output))
                caret += 1
            i += 1
            line = file.readline()
