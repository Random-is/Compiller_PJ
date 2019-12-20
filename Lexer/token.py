from dataclasses import dataclass
from typing import Any


from Lexer.types import TokenType


@dataclass
class Token:
    value: Any
    raw_value: str
    type: TokenType
    line: int
    number: int

    def __str__(self):
        return f'{self.line}\t{self.number}\t{self.type.name}\t{self.raw_value}\t{self.value}'

