STATES = 637

EPSILON = 0
UNICODE_LATIN_START = 32
UNICODE_LATIN_END = 127

SEEK_RULE = 1
SEEK_RULE_NAME = 2
SEEK_ST_COLON = 3
SEEK_ND_COLON = 4
SEEK_EQUALS = 5
SEEK_ST_PROD = 6
SEEK_ST_TERM = 7
SEEK_ST_NTERM = 8
SEEK_ST_ESC = 9
SEEK_PROD = 10
SEEK_TERM = 11
SEEK_NTERM = 12
SEEK_ESC = 13

SEEK_SPECIAL_TERM = 14
SEEK_SPECIAL_NTERM = 15
SEEK_SPECIAL_DONE = 16

EXPECTED_LT = -1
EMPTY_RULENAME = -2
LT_FOBIDDEN = -3
EXPECTED_COLON = -4
EXPECTED_EQUALS = -5
EMPY_PRODUCTION = -6
INVALID_TOKEN = -7
INVALID_ESCAPE = -8
DUPLICATED_RULE = -9
INVALID_REGULAR = -10
PLUS_BEFORE = -11

INTERESTING = {50, 49, 9, 46, 14, 18, 15, 44, 21, 22, 30, 31, 20, 33, 34, 35, 17, 39, 16, 41, 42, 23, 26, 27, 28, 19, 36}
VARIABLES = {14, 18, 15, 44, 21, 22, 30, 31, 20, 33, 34, 35, 17, 39, 16, 41, 42, 23, 26, 27, 28, 19, 36}
SYMBOLS = {"", " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "while", "for", "if", "else", "let", "(EOF)", "plus", "minus", "or", "and"}
