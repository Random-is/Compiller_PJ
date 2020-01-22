from Main.error import ParserError, ErrorType
from Lexer.tokenizer import Tokenizer
from Lexer.types import *
from Parser.ast import *


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def error(self, text: str, token: Token):
        raise ParserError(text, token)

    def next(self):
        return self.tokenizer.next()

    def next_b(self):
        token = self.next()
        self.back_t(token)
        return token

    def back_t(self, *tokens: Token):
        for token in tokens:
            self.tokenizer.back_token(token)

    @staticmethod
    def convert_token_param(t_type, t_value=None):
        t_value = t_value if isinstance(t_value, list) else [t_value]
        t_type = t_type if isinstance(t_type, list) else [t_type]
        return t_type, t_value

    @staticmethod
    def check_t(token, t_type, t_value=None):
        t_type, t_value = Parser.convert_token_param(t_type, t_value)
        return token.type in t_type and (t_value == [None] or token.value in t_value)

    def req(self, t_type, t_value=None):
        token = self.next()
        if not self.check_t(token, t_type, t_value):
            t_type, t_value = self.convert_token_param(t_type, t_value)
            self.error(ErrorType.EXPECTED.info(*(t_type if t_value == [None] else t_value)), token)
        return token

    def req_var_type(self):
        if self.is_type(token := self.next()):
            return NodeKeyWord(token)
        elif self.check_t(token, TokenType.IDENT):
            return NodeIdent(token)
        else:
            self.error(ErrorType.VAR_TYPE_EX.value, token)

    def is_type(self, token: Token):
        return self.check_t(token, TokenType.KEY_WORD, [KeyWordType.INT, KeyWordType.DOUBLE, KeyWordType.CHAR,
                                                        KeyWordType.BOOLEAN, KeyWordType.VOID])

    def compilation_unit(self):
        class_node = self.class_decl() if not self.check_t(self.next_b(), TokenType.EOF) else NodeNone()
        return NodeCompUnit(class_node)

    def class_decl(self):
        self.req(TokenType.KEY_WORD, KeyWordType.CLASS)
        name = self.identifier()
        self.req(TokenType.SEPARATOR, SepType.L_CURLY)
        fields = self.fields()
        self.req(TokenType.SEPARATOR, SepType.R_CURLY)
        return NodeClass(name, fields)

    def fields(self):
        block = []
        while not self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_CURLY):
            block.append(self.field_decl())
        return NodeBlock(block if block else [NodeNone()])

    def field_decl(self):
        t_1 = self.next()
        if self.check_t(t_1, TokenType.SEPARATOR, SepType.SEMI):
            return NodeNone()
        elif self.check_t(t_1, TokenType.KEY_WORD, KeyWordType.VOID):  # Method
            self.back_t(t_1)
            return self.method_decl()
        elif self.is_type(t_1) or self.check_t(t_1, TokenType.IDENT):
            if self.is_method():
                self.back_t(t_1)
                return self.method_decl()
            elif self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_PARENT):
                self.back_t(t_1)
                return self.constructor_decl()
            else:
                self.back_t(t_1)
                var = self.var_decl()
                self.req(TokenType.SEPARATOR, SepType.SEMI)
                return var
        elif self.check_t(t_1, TokenType.SEPARATOR, SepType.R_CURLY):
            self.back_t(t_1)
            return NodeNone()
        else:
            self.error(ErrorType.UNEXPECTED_TOKEN.value, t_1)

    def var_decl(self):
        if self.is_type(t_1 := self.next()):
            var_type = NodeKeyWord(t_1)
        else:
            var_type = NodeIdent(t_1)
        name = self.identifier()
        t_1 = self.next()
        if self.check_t(t_1, TokenType.SEPARATOR, SepType.SEMI):  # Variable
            self.back_t(t_1)
            return NodeVar(var_type, name, NodeNone())
        elif self.check_t(t_1, TokenType.OPERATION, OpType.ASSIGN):  # Variable = expr
            return NodeVar(var_type, name, self.var_init())
        elif self.check_t(t_1, TokenType.SEPARATOR, SepType.L_BRACKET):  # Variable[]
            self.req(TokenType.SEPARATOR, SepType.R_BRACKET)
            t_2 = self.next()
            if self.check_t(t_2, TokenType.OPERATION, OpType.ASSIGN):  # Variable[] = expr
                self.back_t(self.req(TokenType.SEPARATOR, SepType.L_CURLY))
                value = self.var_init()
                return NodeVar(var_type, name, value)
            self.back_t(t_2)
            return NodeVar(var_type, name, NodeBlock([NodeNone()]))
        else:
            self.back_t(t_1)
            self.req(TokenType.SEPARATOR, SepType.SEMI)

    def method_init(self):
        name = self.identifier()
        self.req(TokenType.SEPARATOR, SepType.L_PARENT)
        params = self.parameter_list()
        self.req(TokenType.SEPARATOR, SepType.R_PARENT)
        statements = self.statement_block()
        return name, params, statements

    def method_decl(self):
        return_type = self.req_var_type()
        name, params, statements = self.method_init()
        return NodeMethod(return_type, name, params, statements)

    def constructor_decl(self):
        name, params, statements = self.method_init()
        return NodeConstr(name, params, statements)

    def statement_block(self):
        self.req(TokenType.SEPARATOR, SepType.L_CURLY)
        block = []
        while not self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_CURLY):
            block.append(self.statement())
        self.req(TokenType.SEPARATOR, SepType.R_CURLY)
        return NodeBlock(block if block else [NodeNone()])

    def statement(self):
        return NodeNone()

    def parameter_list(self):
        if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_PARENT):
            return NodeBlock([NodeNone()])
        block = [self.parameter()]
        while self.check_t(token := self.next(), TokenType.SEPARATOR, SepType.COMMA):
            block.append(self.parameter())
        self.back_t(token)
        return NodeBlock(block)

    def parameter(self):
        var_type = self.req_var_type()
        name = self.identifier()
        if self.check_t(token := self.next(), TokenType.SEPARATOR, SepType.L_BRACKET):
            self.req(TokenType.SEPARATOR, SepType.R_BRACKET)
            return NodeVar(var_type, name, NodeBlock([NodeNone()]))
        self.back_t(token)
        return NodeVar(var_type, name, NodeNone())

    def is_method(self):
        t_1, t_2 = self.next(), self.next()
        self.back_t(t_2, t_1)
        return self.check_t(t_1, TokenType.IDENT) and self.check_t(t_2, TokenType.SEPARATOR, SepType.L_PARENT)

    def var_init(self):
        token = self.next()
        if self.check_t(token, TokenType.SEPARATOR, SepType.L_CURLY):
            if self.check_t(t := self.next(), TokenType.SEPARATOR, SepType.R_CURLY):
                return NodeBlock([NodeNone()])
            self.back_t(t)
            block = [self.var_init()]
            while self.check_t(token := self.next(), TokenType.SEPARATOR, SepType.COMMA):
                block.append(self.var_init())
            self.back_t(token)
            self.req(TokenType.SEPARATOR, SepType.R_CURLY)
            return NodeBlock(block)
        else:
            self.back_t(token)
            return self.expr()

    def expr(self):
        node = self.term()
        while self.check_t(token := self.next(), TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            node = NodeBinOp(token, node, self.term())
        self.back_t(token)
        return node

    def term(self):
        node = self.factor()
        while self.check_t(token := self.next(), TokenType.OPERATION, [OpType.MUL, OpType.DIV]):
            node = NodeBinOp(token, node, self.factor())
        self.back_t(token)
        return node

    def factor(self):
        token = self.tokenizer.next()
        if self.check_t(token, TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            return NodeUnaryOp(token, self.factor())
        elif self.check_t(token, [TokenType.INT, TokenType.DOUBLE]):
            return NodeLiteral(token)
        elif self.check_t(token, TokenType.IDENT):
            return NodeIdent(token)
        elif self.check_t(token, TokenType.SEPARATOR, SepType.L_PARENT):
            node = self.expr()
            self.req(TokenType.SEPARATOR, SepType.R_PARENT)
            return node
        else:
            self.error(ErrorType.EXPECTED.info(SepType.L_PARENT, OpType.PLUS, OpType.MINUS, TokenType.DOUBLE,
                                               TokenType.INT, TokenType.IDENT), token)

    def identifier(self):
        return NodeIdent(self.req(TokenType.IDENT))

    def parse(self):
        return self.compilation_unit()
