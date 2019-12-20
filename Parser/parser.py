from Lexer.token import Token
from Lexer.types import TokenType, OpType
from Parser.ast import NodeLiteral, NodeBinOp, NodeUnaryOp, NodeBlock, NodeIdent

"""
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | LPAREN expr RPAREN
"""


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def error(self, token, text):
        raise Exception('Syntax error at {0}:{1} {2} {3}\n\t{4}'.format(token.line,
                                                                        token.number,
                                                                        token.type.name,
                                                                        token.value,
                                                                        text))

    def req_next(self, text, req_type, req_value=None):
        req_values = []
        if req_value is not None:
            if isinstance(req_value, list):
                req_values = req_value
            else:
                req_values.append(req_value)
        token = self.tokenizer.next()
        if token.type != req_type:
            self.error(token, text)
        elif req_value is not None and token.value not in req_values:
            self.error(token, text)
        else:
            return token

    def program(self):
        """program : compound_statement DOT"""
        self.req_next('private/public required', TokenType.KEY_WORD, ['public', 'private'])
        self.req_next('class required', TokenType.KEY_WORD, 'class')
        return NodeUnaryOp(self.req_next('Class NAME required', TokenType.IDENT), self.compound_statement())

    def compound_statement(self):
        """compound_statement: BEGIN statement_list END"""
        token = self.req_next('{ required', TokenType.SEPARATOR, '{')
        nodes = self.statement_list()
        self.req_next('} required', TokenType.SEPARATOR, '}')
        return NodeBlock(token, nodes)

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        statements = []
        token = self.tokenizer.next_back()
        while token.value != '}' and token.type != TokenType.EOF:
            if (statement := self.statement()) is not None:
                if not isinstance(statement, NodeBlock):
                    self.req_next('; required', TokenType.SEPARATOR, ';')
                statements.append(statement)
            token = self.tokenizer.next_back()
        self.tokenizer.back_token(token)
        return statements

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        token = self.tokenizer.next_back()
        if token.value == '{':
            node = self.compound_statement()
        elif token.type == TokenType.IDENT:
            node = self.assignment_statement()
        elif token.value == '}' or token.type == TokenType.EOF:
            node = None
        else:
            self.error(token, 'NOT SUPPORT RIGHT NOW')
        return node

    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.req_next('Assigment required', TokenType.OPERATION, '=')
        right = self.expr()
        return NodeBinOp(token, left, right)

    def variable(self):
        """variable : ID"""
        return NodeIdent(self.req_next('Variable NAME required', TokenType.IDENT))

    def expr(self):
        node = self.term()
        while (token := self.tokenizer.next()).value in (OpType.PLUS.value, OpType.MINUS.value):
            node = NodeBinOp(token, node, self.term())
        self.tokenizer.back_token(token)
        return node

    def term(self):
        node = self.factor()
        while (token := self.tokenizer.next()).value in (OpType.MUL.value, OpType.DIV.value):
            node = NodeBinOp(token, left=node, right=self.factor())
        self.tokenizer.back_token(token)
        return node

    def factor(self):
        token = self.tokenizer.next()
        if token.value in (OpType.PLUS.value, OpType.MINUS.value):
            return NodeUnaryOp(token, arg=self.factor())
        elif token.type == TokenType.VAR_VALUE:
            return NodeLiteral(token)
        elif token.value == "(":
            node = self.expr()
            self.req_next(') required', TokenType.SEPARATOR, ')')
            return node
        else:
            self.error(token, 'expr required')

    def parse(self):
        return self.program()
