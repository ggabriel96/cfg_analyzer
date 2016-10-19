from const import *
from GrammarError import *
from collections import OrderedDict

class NDFA():
    def __init__(self):
        self.dfa = None
        self.ndfa = [OrderedDict()]
        self.labels = {}

    @classmethod
    def builtWith(cls, grammar):
        self = cls()
        self.build(grammar)
        return self

    def eps_closure(self, state):
        stack = [ state ]
        closure = {state}
        while len(stack) > 0:
            t = stack.pop()
            if 0 in self.ndfa[t]:
                for s in self.ndfa[t][0]:
                    stack.append(s)
                    closure.add(s)
        return closure

    def eps_closure_set(self, state_set):
        closure_set = set()
        for state in state_set:
            closure = self.eps_closure(state)
            for cl in closure:
                closure_set.add(cl)
        return closure_set

    def to_dfa(self):
        print(self.eps_closure_set({6, 9}))

    def build(self, grammar):
        encode = {}
        finalname = {}
        terminal_number = 0
        for rule, productions in grammar.rules.items():
            print(rule)
            if rule in grammar.asterisk or rule in grammar.ignore:
                if rule in grammar.asterisk:
                    state = 0
                    finalname[rule] = len(self.ndfa)
                    self.labels[finalname[rule]] = rule
                    self.ndfa.append(OrderedDict())
                else:
                    if rule not in encode:
                        state = encode[rule] = len(self.ndfa)
                        self.ndfa.append(OrderedDict())
                    else:
                        state = encode[rule]
                for production in productions:
                    final = None
                    trans_sym = None
                    machine_state = SEEK_SPECIAL_TERM
                    for symbol in production:
                        if machine_state == SEEK_SPECIAL_TERM:
                            if symbol.isterm:
                                trans_sym = symbol
                                machine_state = SEEK_SPECIAL_NTERM
                            else:
                                raise GrammarError.withMessage(INVALID_REGULAR, "'{}'".format(rule))
                        elif machine_state == SEEK_SPECIAL_NTERM:
                            if not symbol.isterm:
                                if rule not in finalname:
                                    raise GrammarError.withMessage(PLUS_BEFORE, "'{}'".format(rule))
                                finalname[symbol.name] = finalname[rule]
                                if symbol.name not in encode:
                                    encode[symbol.name] = len(self.ndfa)
                                    self.ndfa.append(OrderedDict())

                                ordsym = ord(trans_sym.name) if trans_sym.name != "" else 0;
                                if ordsym not in self.ndfa[state]:
                                    self.ndfa[state][ordsym] = [ encode[symbol.name] ]
                                else:
                                    self.ndfa[state][ordsym].append(encode[symbol.name])
                                machine_state = SEEK_SPECIAL_DONE
                            else:
                                raise GrammarError.withMessage(INVALID_REGULAR, "'{}'".format(rule))
                    else:
                        if machine_state == SEEK_SPECIAL_NTERM:
                            if rule not in finalname:
                                raise GrammarError.withMessage(PLUS_BEFORE, "'{}'".format(rule))
                            ordsym = ord(symbol.name) if symbol.name != "" else 0;
                            if ordsym not in self.ndfa[state]:
                                self.ndfa[state][ordsym] = [ finalname[rule] ]
                            else:
                                self.ndfa[state][ordsym].append(finalname[rule])
            else:
                final = None
                for production in productions:
                    for symbol in production:
                        if symbol.isterm and symbol.name != "":
                            if final == None:
                                final = len(self.ndfa)
                                self.ndfa.append(OrderedDict())
                                self.labels[final] = rule
                                # print("final: {}".format(rule))
                            state = 0
                            for i, c in enumerate(symbol.name):
                                # print("{}: {}".format(c, ord(c)))
                                if i == len(symbol.name) - 1:
                                    if ord(c) not in self.ndfa[state]:
                                        self.ndfa[state][ord(c)] = [ final ]
                                    else:
                                        self.ndfa[state][ord(c)].append(final)
                                else:
                                    prox = len(self.ndfa)
                                    self.ndfa.append(OrderedDict())
                                    if ord(c) not in self.ndfa[state]:
                                        self.ndfa[state][ord(c)] = [ prox ]
                                    else:
                                        self.ndfa[state][ord(c)].append(prox)
                                    state = prox


    def printndfa(self):
        print("<=========>")
        #print(self.ndfa)
        for i in range(len(self.ndfa)):
            print("State #{}: ".format(i))
            # print(self.ndfa[i]);
            for char, estado in self.ndfa[i].items():
                print("Caracter \'{}\' vai para estado {}".format(chr(char), estado))
            print()

    def printlab(self):
        print("\n\nLabels:")
        for k in self.labels:
            print(k)
