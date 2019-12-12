from dataclasses import dataclass
from typing import Any


from Lexer.types import TokenType


@dataclass
class Token:
    value: Any
    type: TokenType
    line: int
    number: int

    def __str__(self):
        return '{0}\t{1}\t{2}\t{3}'.format(self.line, self.number, self.type.name, self.value)
