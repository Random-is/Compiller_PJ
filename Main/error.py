from enum import Enum

from Lexer.token import Token
from Lexer.types import TokenType


class ErrorType(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Variable is already defined in the Scope'
    NOT_STATEMENT = 'Not a statement'
    EXPECTED = '{} expected'
    VAR_TYPE_EX = EXPECTED.format('Variable Type')

    def info(self, *info: Enum) -> str:
        is_token_type = False if [x for x in info if not isinstance(x, TokenType)] else True
        info = [x.value for x in info]
        info = '"' + '" / "'.join(info) + '"' + (' ' + ('types' if len(info) > 1 else 'return_type') if is_token_type else '')
        return self.value.format(info)


class Error(Exception):
    def __init__(self, err_type: str, token: Token, message: str = ''):
        self.err_type = err_type
        self.token = token
        self.message = f'{self.__class__.__name__}: {err_type} -> {token}\n{message}'


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class SemanticError(Error):
    pass
