import string
from const import *
from file import *

class Synt():
    def __init__(self):
        self.rules = None
        self.ptable = None
        self.buildRules()
        self.buildLALR()
        # print(self.rules)

    def buildRules(self):
        with open('glcrules.htw', 'r') as f:
            tmp = f.read().split('\n')
        tmp.pop()
        self.rules = [None] * len(tmp)
        print("\n\n")
        for line in tmp:
            estado = 0
            index = 0
            cont = 0
            rule = ""
            # print(">>>>" + line)
            for c in line:
                # print("char: {}   estado:  {}".format(c, estado))
                if estado == 0: #Lê o numero
                    if c in string.whitespace:
                        estado = 1
                        continue
                    index *= 10
                    index += int(c)

                if estado == 1: # ignoring whitespaces
                    if c not in string.whitespace:
                        rule = c
                        estado = 2
                        continue

                if estado == 2: # reading the rule name
                    if c in string.whitespace:
                        estado = 3
                        continue
                    rule += c

                if estado == 3: # ignoring everything until '='
                    if c == '=':
                        estado = 4
                        continue

                if estado == 4: # counting productions
                    if c == ' ':
                        cont += 1
            # print("self.rules[{}] = [{}, {}]".format(index, rule, cont))
            self.rules[index] = [rule, cont]

    def buildLALR(self):
        self.ptable = [None] * STATES
        f = File('lalr.htw')
        for i in range(STATES):
            f.readline()
            state = None
            self.ptable[i] = {}
            symbol = f.getNextWord()
            while symbol != 'State':
                action = f.getNextWord()
                if action != 'a':
                    state = f.getNextInt()
                # print("{}: {} {} {}".format(i, symbol, action, state))
                self.ptable[i][symbol] = [action, state]
                symbol = f.getNextWord()
        # print(self.ptable)
        # print(self.ptable[38])
