from Lexer.types import TokenType
from Parser.ast import NodeLiteral, NodeBinOp

"""
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | LPAREN expr RPAREN
"""


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def expr(self):
        node = self.term()
        while (token := self.tokenizer.next()).value in ("+", "-"):
            node = NodeBinOp(token, left=node, right=self.term())
        self.tokenizer.back_token(token)
        return node

    def term(self):
        node = self.factor()
        while (token := self.tokenizer.next()).value in ("*", "/"):
            node = NodeBinOp(token, left=node, right=self.factor())
        self.tokenizer.back_token(token)
        return node

    def factor(self):
        token = self.tokenizer.next()
        if token.type == TokenType.VAR_VALUE:
            return NodeLiteral(token)
        elif token.value == "(":
            node = self.expr()
            token = self.tokenizer.next()
            if token.value == ")":
                return node

    def parse(self):
        return self.expr()
