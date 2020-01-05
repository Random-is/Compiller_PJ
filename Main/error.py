from enum import Enum

from Lexer.token import Token
from Lexer.types import TokenType


class ErrorType(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'variable is already defined'
    EXPECTED = '{} expected'

    def info(self, info) -> str:
        is_token_type = isinstance(info[0], TokenType)
        info = [x.value for x in info] if isinstance(info, list) else [info.value]
        info = '/'.join(info) + (' ' + ('types' if len(info) > 1 else 'type') if is_token_type else '')
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
