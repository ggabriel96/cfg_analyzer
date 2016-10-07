#!/bin/python3.5
import sys
from analyzer import *

def main(argv):
    # The with statement allows objects like files to be used in a way
    # that ensures they are always cleaned up promptly and correctly.
    with open(argv[1], 'r') as f:
        read_grammar(f)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv);
