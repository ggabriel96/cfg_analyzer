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
                if char == ' ':
                    continue
                    # newline += chr(1)
                    # state = CHAR2
                elif char == '"':
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
                c = ord(char)
                print("current_state: {}\nchar '{}': {}".format(current_state, char if char != '\n' else "\\n", c))
                token_end += 1
                if char in self.separators:
                    print("in separators")
                    if current_state not in self.dfa.finals and c not in self.dfa.table[current_state]:
                        raise LexicalError(INVALID_TOKEN, i, "'{}'".format(line[token_start:token_end]))
                    if c not in self.dfa.table[current_state] or wasFinal:
                        self.output.append(current_state)
                        token_start = token_end
                        if c in self.dfa.table[0]:
                            print("isFinal\ntransition from {} to {} through '{}'".format(current_state, self.dfa.table[0][c], char))
                            current_state = self.dfa.table[0][c]
                            wasFinal = True
                            caret += 1
                        else:
                            print("reset")
                            current_state = 0
                            if char == '\n':
                                caret += 1
                        print("output: {}\n\n".format(self.output))
                        continue
                if c in self.dfa.table[current_state]:
                    print("transition from {} to {} through '{}'".format(current_state, self.dfa.table[current_state][c], char))
                    current_state = self.dfa.table[current_state][c]
                elif wasFinal == True and c in self.dfa.table[0]:
                    print("wasFinal")
                    self.output.append(current_state)
                    current_state = self.dfa.table[0][c]
                else:
                    raise LexicalError(INVALID_TOKEN, i, "'{}' not mapped on state {}".format(char, current_state))
                wasFinal = False
                print("output: {}\n\n".format(self.output))
                caret += 1
            i += 1
            line = file.readline()
