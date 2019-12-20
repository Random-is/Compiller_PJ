from enum import Enum, auto


class StateType(Enum):
    START = auto()
    LESS = auto()
    MORE = auto()
    NOT = auto()
    R_SLASH_CHAR = auto()
    R_SLASH_STR = auto()
    SLASH = auto()
    COMMENT = auto()
    STRING = auto()
    CHAR = auto()
    END_CHAR = auto()
    OR = auto()
    AND = auto()
    EQUALS = auto()
    MINUS = auto()
    ZERO = auto()
    INT = auto()
    DOUBLE = auto()
    WORD = auto()


class TokenType(Enum):
    SEPARATOR = auto()
    OPERATION = auto()
    KEY_WORD = auto()
    IDENT = auto()
    INT = auto()
    DOUBLE = auto()
    BOOLEAN = auto()
    CHAR = auto()
    STRING = auto()
    EXCEPTION = auto()
    EOF = auto()


class OpType(Enum):
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'


class SepType(Enum):
    L_CURLY = '{'
    R_CURLY = '}'
    L_BRACKET = '['
    R_BRACKET = ']'
    L_PARENT = '('
    R_PARENT = ')'
    SEMI = ';'
    POINT = '.'
    COMMA = ','


class BoolType(Enum):
    TRUE = 'True'
    FALSE = 'False'


class KeyWordType(Enum):
    IF = 'if'
    ABSTRACT = 'abstract'
    ASSERT = 'assert'
    BOOLEAN = 'boolean'
    BREAK = 'break'
    BYTE = 'byte'
    CASE = 'case'
    CATCH = 'catch'
    CHAR = 'char'
    CLASS = 'class'
    CONST = 'const'
    CONTINUE = 'continue'
    DEFAULT = 'default'
    DO = 'do'
    DOUBLE = 'double'
    ELSE = 'else'
    ENUM = 'enum'
    EXTENDS = 'extends'
    FINAL = 'final'
    FINALLY = 'finally'
    FLOAT = 'float'
    FOR = 'for'
    GOTO = 'goto'
    IMPLEMENTS = 'implements'
    IMPORT = 'import'
    INSTANCEOF = 'instanceof'
    INT = 'int'
    INTERFACE = 'interface'
    LONG = 'long'
    NATIVE = 'native'
    NEW = 'new'
    PACKAGE = 'package'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    PUBLIC = 'public'
    RETURN = 'return'
    SHORT = 'short'
    STATIC = 'static'
    STRICTFP = 'strictfp'
    SUPER = 'super'
    SWITCH = 'switch'
    SYNCHRONIZED = 'synchronized'
    THIS = 'this'
    THROW = 'throw'
    THROWS = 'throws'
    TRANSIENT = 'transient'
    TRY = 'try'
    VOID = 'void'
    VOLATILE = 'volatile'
    WHILE = 'while'
    NULL = 'null'
