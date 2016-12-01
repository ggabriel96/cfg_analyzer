import string
from decimal import *

class File:
    def __init__(self, path):
        self.f = open(path, 'r')

    def read(self, n):
        return self.f.read(n)

    def readline(self):
        return self.f.readline()

    def close(self):
        self.f.close()

    # Returns nextInt in the file
    def getNextInt(self):
        word = self.f.read(1)
        while word in string.whitespace and len(word) > 0: # Ignores white spaces (tab, space, \n) and get the first char
            word = self.f.read(1)
        tmp = word; num = ""
        while tmp.isnumeric() and len(tmp) > 0: # Reads the number
            num += tmp
            tmp = self.f.read(1)
        return int(num) if len(num) > 0 else 0

    def getNextWord(self):
        word = self.f.read(1)
        while word in string.whitespace and len(word) > 0: # Ignores white spaces (tab, space, \n) and get the first char
            word = self.f.read(1)
        tmp = self.f.read(1)
        while tmp not in string.whitespace and len(tmp) > 0: # Reads the word
            word += tmp
            tmp = self.f.read(1)
        return word
