class NDFA():
    def __init__(self, grammar, asterisk):
        self.dfa = None
        self.ndfa = [{}, {}] #Inicializo já os dois primeiros estados, por causa da forma como faço
        self.encode = {}
        self.decode = {}
        self.build(grammar, asterisk)

    def build(self, grammar, asterisk):
        cont = 0 #Used to give a number to a terminal
        state = 1
        for rule, productions in grammar.items():
            if rule in asterisk:
                continue
            for production in productions:
                for symbol in production:
                    if symbol.isterm and symbol.name not in self.encode and symbol.name != "":
                        self.encode[symbol.name] = cont
                        self.decode[cont] = symbol.name
                        first = True
                        for c in symbol.name:
                            if first:
                                if state == 0:
                                    print("AQUI CARALEO: {} : {}".format(rule, ord(c)))
                                if ord(c) not in self.ndfa[0]:
                                    self.ndfa[0][ord(c)] = []
                                #self.ndfa.append({})
                                self.ndfa[0][ord(c)].append(state)
                                #state += 1
                                first = False
                            else:
                                if state == 0:
                                    print("AQUI CARALEO2: {} : {}".format(rule, ord(c)))
                                self.ndfa.append({})
                                self.ndfa[state][ord(c)] = state + 1
                                state += 1
                        self.ndfa.append({}) #É o estado final de reconhecimento do token
                        state += 1
                        cont += 1
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
