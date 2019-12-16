from enum import Enum


class StateType(Enum):
    START = 0
    LESS = 1
    MORE = 2
    NOT = 3
    R_SLASH = 4
    SLASH = 5
    COMMENT = 6
    STRING = 7
    OR = 8
    AND = 9
    EQUALS = 10
    MINUS = 11
    ZERO = 12
    INT = 13
    DOUBLE = 14
    WORD = 15


class TokenType(Enum):
    SEPARATOR = 0
    OPERATION = 1
    KEY_WORD = 2
    VAR_NAME = 3
    VAR_VALUE = 4
    EXCEPTION = 5
    EOF = 6


class OpType(Enum):
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'


class KeyWordType(Enum):
    IF = 'if'
