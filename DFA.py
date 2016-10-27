from const import *
from GrammarError import *
from collections import OrderedDict

class DFA():
    def __init__(self):
        self.table = [ OrderedDict() ]
        self.finals = set()

    def printdfa(self):
        print("\nDFA:")
        for i in range(len(self.table)):
            print("State #{}: ".format(i))
            for char, estado in self.table[i].items():
                print("Caracter \'{}\' vai para estado {}".format(chr(char), estado))
            print()

    def is_final(self, state):
        if state in self.finals:
            return True
        return False

    def to_csv(self):
        csv = ", eps"
        for char in range(UNICODE_LATIN_START, UNICODE_LATIN_END):
            if char < UNICODE_LATIN_END:
                csv += ", "
            c = chr(char)
            if c == '"':
                csv += "\"\"\"\""
            elif c == ',':
                csv += "\",\""
            else:
                csv += "{}".format(c)
        for state, rule in enumerate(self.table):
            csv += "\n{}".format(state)
            csv += ", {}".format(rule[0] if 0 in rule else "X")
            for char in range(UNICODE_LATIN_START, UNICODE_LATIN_END):
                if char < UNICODE_LATIN_END:
                    csv += ", "
                csv += "{}".format(rule[char] if char in rule else "X")
        csv += "\n"
        return csv
