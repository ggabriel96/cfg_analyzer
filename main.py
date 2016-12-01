#!/bin/python3.5
import sys
from Grammar import *
from Parser import *
from NDFA import *
from DFA import *
from Synt import *

def main(argv):
    # The with statement allows objects like files to be used in a way
    # that ensures they are always cleaned up promptly and correctly.
    with open(argv[1], 'r') as f:
        a = Grammar()
        a.readgr(f)
    # print("\nSpecial states:"); print(a.asterisk)
    # print("\nSpecial states children:"); print(a.ignore)
    # print("\nGrammar:"); a.printgr()

    b = NDFA().builtWith(a)
    # print("NDFA:"); b.printndfa()
    # print("ndfa final states: {}".format(b.finals))
    # print(b.to_csv())

    c = b.to_dfa()
    # print("DFA:"); c.printdfa()
    # print("\nDFA final states: {}\n".format(c.finals))
    # print(c.to_csv())

    p = Parser(c)
    if argv[2] is not None:
        with open(argv[2], 'r') as f:
            p.parse(f)
        print("\nSymbol table: {}\n".format (p.table))
    else:
        print("No source code input")

    d = Synt().fromParser(p)
    d.reckon()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv);
