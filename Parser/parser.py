from Main.error import ParserError, ErrorType
from Lexer.tokenizer import Tokenizer
from Lexer.types import *
from Parser.type import Array, Primitive, Type, Void
from Parser.ast import *


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.type_table = {
            KeyWordType.INT.value: Primitive(0, KeyWordType.INT.value),
            KeyWordType.DOUBLE.value: Primitive(0.0, KeyWordType.DOUBLE.value),
            KeyWordType.CHAR.value: Primitive('', KeyWordType.CHAR.value),
            KeyWordType.STRING.value: Primitive('', KeyWordType.STRING.value),
            KeyWordType.BOOLEAN.value: Primitive(False, KeyWordType.BOOLEAN.value)
        }

    # region Utility

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

    def _type(self):
        token = self.next()
        if not self.is_type(token):
            self.error(ErrorType.VAR_TYPE_EX.value, token)
        _type = self.type_table[token.raw_value]
        while self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_BRACKET):
            self.req(TokenType.SEPARATOR, SepType.L_BRACKET)
            self.req(TokenType.SEPARATOR, SepType.R_BRACKET)
            _type = Array(None, _type)
        return _type

    def is_type(self, token: Token):
        return token.raw_value in self.type_table

    def is_block_not_end(self, token: Token):
        return (not self.check_t(token, TokenType.SEPARATOR, SepType.R_CURLY) and
                not self.check_t(token, TokenType.EOF))

    # endregion

    def compilation_unit(self):
        if self.check_t(self.next_b(), TokenType.EOF):
            return NodeNone()
        _class = self._class()
        return NodeCompUnit(_class)

    def _class(self):
        self.req(TokenType.KEY_WORD, KeyWordType.CLASS)
        name = self.identifier()
        self.req(TokenType.SEPARATOR, SepType.L_CURLY)
        fields = self.fields()
        self.req(TokenType.SEPARATOR, SepType.R_CURLY)
        return NodeClass(name, fields)

    def fields(self):
        block = []
        while self.is_block_not_end(self.next_b()):
            block.append(self.field())
        return NodeBlock(block)

    def field(self):
        token = self.next()
        if self.check_t(token, TokenType.SEPARATOR, SepType.SEMI):
            return NodeNone()
        elif self.check_t(token, TokenType.KEY_WORD, KeyWordType.VOID):  # Method
            _type = Void(None)
            name = self.identifier()
            return self.method_decl(_type, name)
        elif self.is_type(token):
            self.back_t(token)
            _type = self._type()
            name = self.identifier()
            if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_PARENT):
                return self.method_decl(_type, name)
            return self.var_decl(_type, name)
        else:
            self.error(ErrorType.UNEXPECTED_TOKEN.value, token)

    # region Method

    def method_decl(self, _type: Type, name: NodeIdent):
        params, statements = self.method_init()
        return NodeMethod(_type, name, params, statements)

    def method_init(self):
        self.req(TokenType.SEPARATOR, SepType.L_PARENT)
        params = self.parameter_list()
        self.req(TokenType.SEPARATOR, SepType.R_PARENT)
        self.req(TokenType.SEPARATOR, SepType.L_CURLY)
        statements = self.statements()
        self.req(TokenType.SEPARATOR, SepType.R_CURLY)
        return params, statements

    def parameter_list(self):
        if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_PARENT):
            return NodeBlock([])
        block = [self.parameter()]
        while self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.COMMA):
            self.req(TokenType.SEPARATOR, SepType.COMMA)
            block.append(self.parameter())
        return NodeBlock(block)

    def parameter(self):
        var_type = self._type()
        name = self.identifier()
        return NodeVar(var_type, name, NodeNone())

    def statements(self):
        block = []
        while self.is_block_not_end(self.next_b()):
            block.append(self.statement())
        return NodeBlock(block)

    def statement(self):
        token = self.next()
        if self.is_type(token):
            self.back_t(token)
            _type = self._type()
            name = self.identifier()
            return self.var_decl(_type, name)
        elif self.check_t(token, TokenType.IDENT):  # var = *; / method_name()
            self.back_t(token)
            name = self.identifier()
            if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_PARENT):  # method_name()
                method = self.method_call(name)
                self.req(TokenType.SEPARATOR, SepType.SEMI)
                return method
            return self.assign(name)  # var = *;
        elif self.check_t(token, TokenType.KEY_WORD, KeyWordType.IF):
            self.req(TokenType.SEPARATOR, SepType.L_PARENT)
            expr = self.expr()
            self.req(TokenType.SEPARATOR, SepType.R_PARENT)
            self.req(TokenType.SEPARATOR, SepType.L_CURLY)
            statements = self.statements()
            self.req(TokenType.SEPARATOR, SepType.R_CURLY)
            else_statements = NodeBlock([])
            if self.check_t(self.next_b(), TokenType.KEY_WORD, KeyWordType.ELSE):
                self.req(TokenType.KEY_WORD, KeyWordType.ELSE)
                self.req(TokenType.SEPARATOR, SepType.L_CURLY)
                else_statements = self.statements()
                self.req(TokenType.SEPARATOR, SepType.R_CURLY)
            return NodeIf(token, expr, statements, else_statements)
        elif self.check_t(token, TokenType.KEY_WORD, KeyWordType.FOR):
            for_init = NodeNone()
            expr = NodeNone()
            for_update = NodeNone()
            self.req(TokenType.SEPARATOR, SepType.L_PARENT)
            if not self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.SEMI):
                for_init = self.for_int()
            self.req(TokenType.SEPARATOR, SepType.SEMI)
            if not self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.SEMI):
                expr = self.expr()
            self.req(TokenType.SEPARATOR, SepType.SEMI)

            if not self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_PARENT):
                for_update = self.for_update()
            self.req(TokenType.SEPARATOR, SepType.R_PARENT)
            self.req(TokenType.SEPARATOR, SepType.L_CURLY)
            statements = self.statements()
            self.req(TokenType.SEPARATOR, SepType.R_CURLY)
            return NodeFor(token, for_init, expr, for_update, statements)
        elif self.check_t(token, TokenType.KEY_WORD, KeyWordType.RETURN):
            ret = NodeReturn(token, self.expr())
            self.req(TokenType.SEPARATOR, SepType.SEMI)
            return ret
        else:
            self.error(ErrorType.NOT_STATEMENT.value, token)

    def for_int(self):
        _type = self._type()
        name = self.identifier()
        self.req(TokenType.OPERATION, OpType.ASSIGN)
        var_init = self.expr()
        return NodeVar(_type, name, var_init)

    def for_update(self):
        name = self.identifier()
        if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_PARENT):  # method_name()
            self.req(TokenType.SEPARATOR, SepType.L_PARENT)
            params = self.argument_list()
            self.req(TokenType.SEPARATOR, SepType.R_PARENT)
            return NodeMCall(name, params)
        else:
            token = self.req(TokenType.OPERATION, OpType.ASSIGN)
            expr = self.expr()
            return NodeAssign(token, name, expr)

    def method_call(self, name: NodeIdent):
        self.req(TokenType.SEPARATOR, SepType.L_PARENT)
        params = self.argument_list()
        self.req(TokenType.SEPARATOR, SepType.R_PARENT)
        # self.req(TokenType.SEPARATOR, SepType.SEMI)
        return NodeMCall(name, params)

    def argument_list(self):
        if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_PARENT):
            return NodeBlock([])
        block = [self.expr()]
        while self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.COMMA):
            self.req(TokenType.SEPARATOR, SepType.COMMA)
            block.append(self.expr())
        return NodeBlock(block)

    def assign(self, name: NodeIdent):
        token = self.req(TokenType.OPERATION, OpType.ASSIGN)
        expr = self.expr()
        self.req(TokenType.SEPARATOR, SepType.SEMI)
        return NodeAssign(token, name, expr)

    # endregion

    # region Variable

    def var_decl(self, _type: Type, name: NodeIdent):
        token = self.next()
        if self.check_t(token, TokenType.SEPARATOR, SepType.SEMI):  # Variable
            return NodeVar(_type, name, NodeNone())
        elif self.check_t(token, TokenType.OPERATION, OpType.ASSIGN):  # Variable = expr
            var_init = self.var_init()
            self.req(TokenType.SEPARATOR, SepType.SEMI)
            return NodeVar(_type, name, var_init)
        else:
            self.back_t(token)
            self.req(TokenType.SEPARATOR, SepType.SEMI)

    def var_init(self):
        token = self.next()
        if self.check_t(token, TokenType.SEPARATOR, SepType.L_CURLY):
            if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.R_CURLY):
                self.req(TokenType.SEPARATOR, SepType.R_CURLY)
                return NodeArrInit([NodeNone()])
            block = [self.var_init()]
            while self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.COMMA):
                self.req(TokenType.SEPARATOR, SepType.COMMA)
                block.append(self.var_init())
            self.req(TokenType.SEPARATOR, SepType.R_CURLY)
            return NodeArrInit(block)
        else:
            self.back_t(token)
            return self.expr()

    # endregion

    def expr(self):
        return self.conditional_or_expression()

    def conditional_or_expression(self):
        node = self.conditional_and_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION, OpType.OR):
            node = NodeBinOp(token, node, self.conditional_and_expression())
        self.back_t(token)
        return node

    def conditional_and_expression(self):  # &&
        node = self.equality_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION, OpType.AND):
            node = NodeBinOp(token, node, self.equality_expression())
        self.back_t(token)
        return node

    def equality_expression(self):  # == / !=
        node = self.relational_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION, [OpType.EQUALS, OpType.NOT_EQUALS]):
            node = NodeBinOp(token, node, self.relational_expression())
        self.back_t(token)
        return node

    def relational_expression(self):  # < > <= >=
        node = self.additive_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION,
                           [OpType.MORE, OpType.MORE_EQUALS, OpType.LESS, OpType.LESS_EQUALS]):
            node = NodeBinOp(token, node, self.additive_expression())
        self.back_t(token)
        return node

    def additive_expression(self):  # + -
        node = self.multiplicative_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            node = NodeBinOp(token, node, self.multiplicative_expression())
        self.back_t(token)
        return node

    def multiplicative_expression(self):  # * / %
        node = self.unary_expression()
        while self.check_t(token := self.next(), TokenType.OPERATION, [OpType.MUL, OpType.DIV, OpType.MOD]):
            node = NodeBinOp(token, node, self.unary_expression())
        self.back_t(token)
        return node

    def unary_expression(self):  # -a +a unary_not_+_-
        token = self.next()
        if self.check_t(token, TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            return NodeUnaryOp(token, self.unary_expression())
        self.back_t(token)
        return self.unary_expression_not_plus_minus()

    def unary_expression_not_plus_minus(self):  # !(unary)
        token = self.next()
        if self.check_t(token, TokenType.OPERATION, OpType.NOT):
            return NodeUnaryOp(token, self.unary_expression())
        self.back_t(token)
        return self.primary()

    def primary(self):  # <primary no new array> | <array creation expression>
        if self.check_t(self.next_b(), TokenType.KEY_WORD, KeyWordType.NEW):
            return self.array_creation_expression()
        return self.primary_no_new_array()

    def primary_no_new_array(self):  # literal / ( expr ) / field access / method invocation / array access
        token = self.next()
        if self.check_t(token, [TokenType.INT, TokenType.DOUBLE]):
            return NodeLiteral(token)
        elif self.check_t(token, [TokenType.STRING, TokenType.CHAR]):
            return NodeLiteral(token)
        elif self.check_t(token, TokenType.BOOLEAN):
            return NodeLiteral(token)
        elif self.check_t(token, TokenType.IDENT):
            if self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_PARENT):
                return self.method_call(token)
            elif self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_BRACKET):
                return self.array_access(token)
            return NodeIdent(token)
        elif self.check_t(token, TokenType.SEPARATOR, SepType.L_PARENT):
            node = self.expr()
            self.req(TokenType.SEPARATOR, SepType.R_PARENT)
            return node
        else:
            self.error(ErrorType.EXPECTED.info(SepType.L_PARENT, OpType.PLUS, OpType.MINUS, TokenType.DOUBLE,
                                               TokenType.INT, TokenType.IDENT), token)

    def array_creation_expression(self):  # new <primitive return_type> <dim exprs> <dims>?
        new = self.req(TokenType.KEY_WORD, KeyWordType.NEW)
        token = self.next()
        if not self.is_type(token):
            self.error(ErrorType.VAR_TYPE_EX.value, token)
        _type = self.type_table[token.raw_value]
        arr_lengths = self.array_lengths()
        for i in arr_lengths.children:
            _type = Array(None, _type)
        return NodeNewArr(new, _type, arr_lengths)

    def array_access(self, name: Token):
        return NodeArrItem(name, self.array_lengths())

    def array_lengths(self):
        block = []
        self.req(TokenType.SEPARATOR, SepType.L_BRACKET)
        block.append(self.expr())
        self.req(TokenType.SEPARATOR, SepType.R_BRACKET)
        while self.check_t(self.next_b(), TokenType.SEPARATOR, SepType.L_BRACKET):
            self.req(TokenType.SEPARATOR, SepType.L_BRACKET)
            block.append(self.expr())
            self.req(TokenType.SEPARATOR, SepType.R_BRACKET)
        return NodeBlock(block)

    # endregion

    def identifier(self):
        return NodeIdent(self.req(TokenType.IDENT))

    def parse(self):
        return self.compilation_unit()
