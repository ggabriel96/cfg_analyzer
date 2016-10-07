#!/bin/python3.5
import sys
from analyzer import *

def main(argv):
    f = open(argv[1], 'r')
    read_grammar(f)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv);
