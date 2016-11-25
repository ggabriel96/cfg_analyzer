import string
from const import *
from file import *

class Synt():
    def __init__(self):
        self.tape = None
        self.rules = None
        self.ptable = None
        self.buildRules()
        self.buildLALR()
        # print(self.rules)

    @classmethod
    def fromParser(cls, parser):
        self = cls()
        self.tape = parser.table
        return self

    def buildRules(self):
        with open('glcrules.htw', 'r') as f:
            tmp = f.read().split('\n')
        tmp.pop()
        self.rules = [None] * len(tmp)
        # print("\n\n")
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

    def parse(self, stack, symbol):
        # print("parse")
        # print("stack: {}".format(stack))
        # print("symbol: {}".format(symbol))
        if symbol in self.ptable[stack[len(stack) - 1]]:
            entry = self.ptable[stack[len(stack) - 1]][symbol]
            # print("entry: {}".format(entry))
            action = entry[0]
            target = entry[1]
            if action == 'a':
                # print("ACCEPTED")
                return True
            elif action == 's':
                # print('s')
                stack.append(symbol)
                stack.append(target)
                # print("stack: {}".format(stack))
                return True
            elif action == 'r':
                # print('r')
                for times in range(2 * self.rules[target][1]):
                    stack.pop()
                g = self.ptable[stack[len(stack) - 1]][self.rules[target][0]]
                if g[0] == 'g':
                    stack.append(self.rules[target][0])
                    stack.append(g[1])
                else:
                    raise SyntaxError("Expected action 'g'")
            else:
                raise SyntaxError("Invalid action")
        else:
            raise SyntaxError("Symbol not in parsing table")
        # print("stack: {}".format(stack))
        return False

    def reckon(self):
        e = 0
        stack = [ 0 ]
        while e < len(self.tape[0]):
            elem = self.tape[0][e]
            label = self.tape[elem[2]]['label']
            # print("\nelem: {}".format(elem))
            if elem[0] in INTERESTING:
                i = 0
                while i < len(label):
                    if self.parse(stack, label[i]) == True:
                        i += 1
                e += 1
            else:
                if self.parse(stack, label) == True:
                    e += 1
        self.semantic()

    def lesser_scope(self, known, variable):
        for scope in known[variable["label"]]:
            if variable["scope"] >= scope:
                return False
        return True

    def semantic(self):
        i = 0
        known = {}
        length = len(self.tape[0])
        while i < length:
            # 37 is the class for 'let'
            if self.tape[0][i][0] is not None and self.tape[0][i][0] == 37:
                j = i + 1
                state = 0 # seeking a variable
                while self.tape[0][j][0] != 10:
                    if state == 0 and self.tape[0][j][0] in VARIABLES:
                        if self.tape[self.tape[0][j][2]]["label"] in known and self.tape[self.tape[0][j][2]]["scope"] in known[self.tape[self.tape[0][j][2]]["label"]]:
                            print("Redeclaration of variable '" + self.tape[self.tape[0][j][2]]["label"] + "' at line " + str(self.tape[0][j][1]))
                        # known.add(self.tape[self.tape[0][j][2]]["label"])
                        if self.tape[self.tape[0][j][2]]["label"] not in known:
                            known[self.tape[self.tape[0][j][2]]["label"]] = { self.tape[self.tape[0][j][2]]["scope"] }
                        else:
                            known[self.tape[self.tape[0][j][2]]["label"]].add(self.tape[self.tape[0][j][2]]["scope"])
                        state = 1 # seeking a comma
                    elif state == 1 and self.tape[0][j][0] in VARIABLES and self.tape[self.tape[0][j][2]]["label"] not in known:
                        print("Unknown variable '" + self.tape[self.tape[0][j][2]]["label"] + "' at line " + str(self.tape[0][j][1]))
                    elif state == 1 and self.tape[0][j][0] == 8:
                        state = 0
                    j += 1
                i = j
            elif self.tape[0][i][0] is not None and self.tape[0][i][0] in VARIABLES and (self.tape[self.tape[0][i][2]]["label"] not in known or self.lesser_scope(known, self.tape[self.tape[0][i][2]])):
                print("Unknown variable '" + self.tape[self.tape[0][i][2]]["label"] + "' at line " + str(self.tape[0][i][1]))
            i += 1
