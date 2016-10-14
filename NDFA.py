class NDFA():
    def __init__(self):
        self.dfa = None
        self.ndfa = [{}] # Inicializo já os dois primeiros estados, por causa da forma como faço
        self.labels = {}

    @classmethod
    def builtWith(cls, grammar):
        self = cls()
        self.build(grammar)
        return self

    def build(self, grammar):
        terminal_number = 0
        for rule, productions in grammar.rules.items():
            if rule in grammar.asterisk or rule in grammar.ignore:
                continue
            final = None
            for production in productions:
                for symbol in production:
                    if symbol.isterm and symbol.name != "":
                        if final == None:
                            final = len(self.ndfa)
                            self.ndfa.append({})
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
                                self.ndfa.append({})
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
