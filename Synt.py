import string
from file import *

class Synt():
    def __init__(self):
        print("PAPAPAPAP")
        self.map = {3: '*', 1: '!', 5: '(', 6: ')', 8: ',', 10: ';', 11: '<', 12: '=', 13: '>', 24: '{', 25: '}', 40: 'for', 38: 'if', 29: 'while', 43: 'else', 32: 'or', 37: 'let'}
        self.rules = None
        self.ptable = None
        self.buildRules()
        self.buildLALR()
        #print(self.rules)

    def buildRules(self):
        print("EBAAAA   ")
        with open('glcrules.htw', 'r') as f:
            tmp = f.read().split('\n')
        tmp.pop()
        self.rules = [None] * len(tmp)
        self.ptable = [None] * len(tmp)
        print("\n\n")
        for line in tmp:
            estado = 0
            index = 0
            cont = 0
            rule = ""
            #print(">>>>" + line)
            for c in line:
                #print("char: {}   estado:  {}".format(c, estado))
                if estado == 0: #Lê o numero
                    if c in string.whitespace:
                        estado = 1
                        continue
                    index *= 10
                    index += int(c)

                if estado == 1: #Ignora espaços
                    if c not in string.whitespace:
                        rule = c
                        estado = 2
                        continue

                if estado == 2: #Lê o nome da regra
                    if c in string.whitespace:
                        estado = 3
                        continue
                    rule += c

                if estado == 3: # Ignora tudo até o =
                    if c == '=':
                        estado = 4
                        continue

                if estado == 4: # Conta os espaçoes (quantidade de produções)
                    if c == ' ':
                        cont += 1
            #print("self.rules[{}] = [{}, {}]".format(index, rule, cont))
            self.rules[index] = [rule, cont]

    def buildLALR(self):
        f = File('lalr.htw')
        string = f.getNextWord()
        index = 0
        state = None
        if string == 'State':
            self.ptable[index] = {}
            index = f.getNextInt()
            symbol = f.getNextWord()
            action = f.getNextWord()
            if action != 'a':
                state = f.getNextInt()
            print(index)
            print(symbol)
            print(action)
            print(state)
            self.ptable[index][symbol] = [action, state]
        print(self.ptable[0])
