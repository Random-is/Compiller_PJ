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
    SEPARATOR = 'Separator'
    OPERATION = 'Operation'
    KEY_WORD = 'KeyWord'
    IDENT = 'Identifier'
    INT = 'Integer'
    DOUBLE = 'Double'
    BOOLEAN = 'Boolean'
    CHAR = 'Char'
    STRING = 'String'
    EXCEPTION = 'Exception'
    EOF = 'EOF'


class OpType(Enum):
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    OR = '||'
    OR_ONE = '|'
    AND = '&&'
    AND_ONE = '&'
    EQUALS = '=='
    NOT = '!'
    MOD = '%'
    NOT_EQUALS = '!='
    MORE = '>'
    MORE_EQUALS = '>='
    LESS = '<'
    LESS_EQUALS = '<='


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
    TRUE = 'true'
    FALSE = 'false'


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
    STRING = 'String'
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
