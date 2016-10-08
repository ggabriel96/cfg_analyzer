#!/bin/python3.5
import sys
from Grammar import *
from NDFA import *

def main(argv):
    # The with statement allows objects like files to be used in a way
    # that ensures they are always cleaned up promptly and correctly.
    with open(argv[1], 'r') as f:
        a = Grammar()
        a.readgr(f)
        print("Special states:")
        print(a.asterisk)
        print("Special states children:")
        print(a.ignore)
        print("\nGrammar:")
        a.printgr()
        print("---------------------")
        b = NDFA().builtWith(a)
        print("---------------------")
        b.printndfa()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv);
