class NDFA():
    def __init__(self):
        self.dfa = None
        self.ndfa = [{}, {}] # Inicializo já os dois primeiros estados, por causa da forma como faço
        self.encode = {}
        self.decode = {}

    @classmethod
    def builtWith(cls, grammar):
        self = cls()
        self.build(grammar)
        return self

    def build(self, grammar):
        state = 1
        terminal_number = 0
        for rule, productions in grammar.rules.items():
            if rule in grammar.asterisk:
                continue
            for production in productions:
                for symbol in production:
                    if symbol.isterm and symbol.name not in self.encode and symbol.name != "":
                        first = True
                        self.encode[symbol.name] = terminal_number
                        self.decode[terminal_number] = symbol.name
                        for c in symbol.name:
                            if first:
                                if ord(c) not in self.ndfa[0]:
                                    self.ndfa[0][ord(c)] = []
                                # self.ndfa.append({})
                                self.ndfa[0][ord(c)].append(state)
                                # state += 1
                                first = False
                            else:
                                self.ndfa.append({})
                                self.ndfa[state][ord(c)] = state + 1
                                state += 1
                        self.ndfa.append({}) # É o estado final de reconhecimento do token
                        state += 1
                        terminal_number += 1

    def printndfa(self):
        print(self.decode)
        print("<=========>")
        print(self.ndfa)
        for i in range(len(self.ndfa)):
            print("State #{}: ".format(i))
            # print(self.ndfa[i]);
            for char, estado in self.ndfa[i].items():
                print("Caracter \'{}\' vai para estado {}".format(chr(char), estado))
            print()
