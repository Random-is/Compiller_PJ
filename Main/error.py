from enum import Enum

from Lexer.token import Token


class ErrorType(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'variable is already defined'
    EXPECTED = '"{}" expected'

    def info(self, info) -> str:
        return self.value.format(info.value)


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
