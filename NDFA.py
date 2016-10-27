from DFA import *
from const import *
from GrammarError import *
from collections import OrderedDict

class NDFA():
    def __init__(self):
        # the first-level array holds the states (lines of table)
        # each position in it holds an OrderedDict, which maps
        # a char to destination states (an array)
        self.table = [ OrderedDict() ]
        self.labels = {}

    @classmethod
    def builtWith(cls, grammar):
        self = cls()
        self.build(grammar)
        return self

    def eps_closure(self, state):
        stack = [ state ]
        closure = { state }
        while len(stack) > 0:
            t = stack.pop()
            if 0 in self.table[t]:
                for s in self.table[t][0]:
                    stack.append(s)
                    closure.add(s)
        return closure

    def eps_closure_set(self, state_set_list):
        closure_set = set()
        for state_list in state_set_list:
            for state in state_list:
                closure = self.eps_closure(state)
                for cl in closure:
                    closure_set.add(cl)
        return closure_set

    def eps_closure_list(self, state_list):
        closure_set = set()
        for state in state_list:
            closure = self.eps_closure(state)
            for cl in closure:
                closure_set.add(cl)
        return closure_set

    def printndfa(self):
        print("<=========>")
        for i in range(len(self.table)):
            print("State #{}: ".format(i))
            for char, estado in self.table[i].items():
                print("Caracter \'{}\' vai para estado {}".format(chr(char), estado))
            print()

    def is_final(self, frozen_dstate):
        for dstate in frozen_dstate:
            if dstate in self.labels:
                return True
        return False

    def frozenstr(self, frozen_set):
        string = "("
        for item in frozen_set:
            string += "[" + str(item) + "]"
        return string + ")"

    def to_dfa(self):
        done = set()
        dfa = DFA()
        init_nstate = frozenset({0})
        nstates = [ init_nstate ]
        encode = { init_nstate: 0 }
        encoding = 1
        while len(nstates) > 0:
            nstate = nstates.pop()
            if nstate in done:
                continue
            done.add(nstate)
            print("\nMaking state {} deterministic...".format(self.frozenstr(nstate)))
            for char in list(range(UNICODE_LATIN_START, UNICODE_LATIN_END)):
                dstate = set()
                for ns in nstate:
                    if char in self.table[ns]:
                        print("Through char '{}'...".format(chr(char)))
                        for t in self.table[ns][char]:
                            print("Target '{}'".format(t))
                            dstate.add(t)
                if len(dstate) > 0:
                    frozen_dstate = frozenset(dstate)
                    nstates.append(frozen_dstate)
                    if frozen_dstate not in encode:
                        encode[frozen_dstate] = encoding
                        if encoding >= len(dfa.table):
                            dfa.table.append(OrderedDict())
                        encoding += 1
                    print("dstate: {}, encoded: {}".format(self.frozenstr(frozen_dstate), encode[frozen_dstate]))
                    dfa.table[encode[nstate]][char] = encode[frozen_dstate]
                    if self.is_final(frozen_dstate):
                        dfa.finals.add(encode[frozen_dstate])
        return dfa

    def to_dfa_hopcroft(self):
        dfa = DFA()
        encode = {}
        decode = {}
        encoding = 0
        closure = frozenset(self.eps_closure_set(self.table[0].values()))
        encode[closure] = encoded_cl = encoding; encoding += 1
        decode[0] = closure
        dstates = { encoded_cl }
        unmarked = { encoded_cl }
        while len(unmarked) > 0:
            rule = unmarked.pop()
            for char in list(range(UNICODE_LATIN_START, UNICODE_LATIN_END)):
                closure = set()
                for nstate in decode[rule]:
                    if char in self.table[nstate]:
                        for clstate in self.eps_closure_list(self.table[nstate][char]):
                            closure.add(clstate)
                if len(closure) > 0:
                    closure = frozenset(closure)
                    if closure not in encode:
                        encode[closure] = encoded_cl = encoding
                        if encoding >= len(dfa.table):
                            dfa.table.append(OrderedDict())
                        encoding += 1
                        decode[encoded_cl] = closure
                    else:
                        encoded_cl = encode[closure]
                    if encoded_cl not in dstates:
                        dstates.add(encoded_cl)
                        unmarked.add(encoded_cl)
                    if rule >= len(dfa.table):
                        dfa.table.append(OrderedDict())
                    dfa.table[rule][char] = encoded_cl
        for dstate in range(len(dfa.table)):
            for nstate in decode[dstate]:
                if nstate in self.labels:
                    dfa.finals.add(dstate)
                    break
        return dfa

    def build(self, grammar):
        encode = {}
        finalname = {}
        terminal_number = 0
        for rule, productions in grammar.rules.items():
            print(rule)
            if rule in grammar.asterisk or rule in grammar.ignore:
                if rule in grammar.asterisk:
                    state = 0
                    finalname[rule] = len(self.table)
                    self.labels[finalname[rule]] = rule
                    self.table.append(OrderedDict())
                else:
                    if rule not in encode:
                        state = encode[rule] = len(self.table)
                        self.table.append(OrderedDict())
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
                                    encode[symbol.name] = len(self.table)
                                    self.table.append(OrderedDict())

                                ordsym = ord(trans_sym.name) if trans_sym.name != "" else 0;
                                if ordsym not in self.table[state]:
                                    self.table[state][ordsym] = [ encode[symbol.name] ]
                                else:
                                    self.table[state][ordsym].append(encode[symbol.name])
                                machine_state = SEEK_SPECIAL_DONE
                            else:
                                raise GrammarError.withMessage(INVALID_REGULAR, "'{}'".format(rule))
                    else:
                        if machine_state == SEEK_SPECIAL_NTERM:
                            if rule not in finalname:
                                raise GrammarError.withMessage(PLUS_BEFORE, "'{}'".format(rule))
                            ordsym = ord(symbol.name) if symbol.name != "" else 0;
                            if ordsym not in self.table[state]:
                                self.table[state][ordsym] = [ finalname[rule] ]
                            else:
                                self.table[state][ordsym].append(finalname[rule])
            else:
                final = None
                for production in productions:
                    for symbol in production:
                        if symbol.isterm and symbol.name != "":
                            if final == None:
                                final = len(self.table)
                                self.table.append(OrderedDict())
                                self.labels[final] = rule
                                # print("final: {}".format(rule))
                            state = 0
                            for i, c in enumerate(symbol.name):
                                # print("{}: {}".format(c, ord(c)))
                                if i == len(symbol.name) - 1:
                                    if ord(c) not in self.table[state]:
                                        self.table[state][ord(c)] = [ final ]
                                    else:
                                        self.table[state][ord(c)].append(final)
                                else:
                                    prox = len(self.table)
                                    self.table.append(OrderedDict())
                                    if ord(c) not in self.table[state]:
                                        self.table[state][ord(c)] = [ prox ]
                                    else:
                                        self.table[state][ord(c)].append(prox)
                                    state = prox


    def printndfa(self):
        print("<=========>")
        for i in range(len(self.table)):
            print("State #{}: ".format(i))
            for char, estado in self.table[i].items():
                print("Caracter \'{}\' vai para estado {}".format(chr(char), estado))
            print()

    def printlab(self):
        print("\n\nLabels:")
        print(self.labels)
        # for k in self.labels:
            # print(k)
