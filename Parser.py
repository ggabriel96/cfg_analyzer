from const import *
from LexicalError import *
from collections import OrderedDict

class Parser():
    def __init__(self, dfa):
        self.dfa = dfa
        self.output = []
        self.symbols = {}
        self.separators = {chr(1), " ", "(", ")", "*", "/", "%", "^", "?", ":", "<", "=", ">", "[", "]", "{", "}", ".", ",", ";", "'", "\"", "\n"}

    def spaces(self, line):
        CHAR = 0
        CHAR2 = 1
        QUOTE = 2
        ESC = 3
        state = CHAR
        newline = ""
        for char in line:
            if state == CHAR:
                # if char == ' ':
                    # continue
                    # newline += chr(1)
                    # state = CHAR2
                # elif char == '"':
                if char == '"':
                    newline += char
                    state = QUOTE
                else:
                    newline += char
            # elif state == CHAR2:
            #     if char == ' ':
            #         continue
            #     elif char == '"':
            #         newline += char
            #         state = QUOTE
            #     else:
            #         newline += char
            elif state == QUOTE:
                newline += char
                if char == '\\':
                    state = ESC
                elif char == '"':
                    state = CHAR
            elif state == ESC:
                newline += char
                state = QUOTE
        return newline

    def parse(self, file):
        i = 1
        token_end = 0
        token_start = 0
        current_state = 0
        line = file.readline()
        while line != "":
            line = self.spaces(line)
            print("-------------------------------------\nline: {}".format(line))
            caret = 0
            wasFinal = False
            while caret < len(line):
                char = line[caret]
                # spaces just matter inside strings, so it's
                # safe to ignore them while in initial state
                if char == ' ' and current_state == 0:
                    caret += 1
                    continue
                c = ord(char)
                print("\n({}, '{}')".format(current_state, char if char != '\n' else "\\n"))
                token_end += 1
                if char in self.separators:
                    print("'{}' is a separator".format(char if char != '\n' else "\\n"))
                    # if we're not at a final state and there is no mapping for
                    # this char in the current state, then we found an error
                    if current_state not in self.dfa.finals and c not in self.dfa.table[current_state]:
                        raise LexicalError(INVALID_TOKEN, i, "'{}'".format(line[token_start:token_end]))
                    # but if we're at a final state and still there's no mapping
                    # we simply reached a final state of a separator
                    if c not in self.dfa.table[current_state]:
                        self.output.append(current_state)
                        print("self.output: {}".format(self.output))
                        token_start = token_end
                        if c in self.dfa.table[0]:
                            print("Separator has mapping on initial state: (0, '{}') -> {}".format(char, self.dfa.table[0][c]))
                            current_state = self.dfa.table[0][c]
                            wasFinal = True
                            caret += 1
                        else:
                            print("No mapping on initial state: simply resetting...")
                            current_state = 0
                            if char == '\n':
                                caret += 1
                        # print("Resetting...")
                        # current_state = 0
                        # if char == '\n':
                        #     caret += 1
                        continue
                    if current_state == 0 or wasFinal:
                        print("Initial state or wasFinal is True: ({}, '{}') -> {}".format(current_state, char, self.dfa.table[current_state][c]))
                        current_state = self.dfa.table[current_state][c]
                        # wasFinal was not necessarily True to enter this if
                        wasFinal = True
                        caret += 1
                        continue
                    # elif wasFinal:
                        # print("wasFinal transition from {} to {} through '{}'".format(current_state, self.dfa.table[current_state][c], char))
                        # current_state = self.dfa.table[current_state][c]
                        # caret += 1
                        # continue
                        # self.output.append(self.dfa.table[current_state][c])
                        # token_start = token_end
                        # current_state = 0
                        # wasFinal = False
                        # caret += 1
                        # continue
                # if we're not looking at a separator and there's a mapping for it in the current state...
                if c in self.dfa.table[current_state]:
                    print("({}, '{}') -> {}".format(current_state, char, self.dfa.table[current_state][c]))
                    current_state = self.dfa.table[current_state][c]
                elif wasFinal == True and c in self.dfa.table[0]:
                    print("wasFinal")
                    self.output.append(current_state)
                    current_state = self.dfa.table[0][c]
                else:
                    raise LexicalError(INVALID_TOKEN, i, "'{}' not mapped on state {}".format(char, current_state))
                wasFinal = False
                print("self.output: {}\n".format(self.output))
                caret += 1
            i += 1
            line = file.readline()
