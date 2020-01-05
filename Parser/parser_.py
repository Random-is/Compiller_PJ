from Lexer.token import Token
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType, KeyWordType, SepType, OpType
from Main.error import ParserError, ErrorType
from Parser.ast import *


class Parser:
    def get_modifiers(self):
        modifiers = []
        while self.check_token(self.next_token_b(),
                               TokenType.KEY_WORD,
                               [KeyWordType.PUBLIC, KeyWordType.PRIVATE, KeyWordType.PROTECTED, KeyWordType.STATIC]):
            modifiers.append(NodeKeyWord(self.next_token()))
        modifiers = modifiers if modifiers else [NodeNone()]
        return NodeMod(modifiers)

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def error(self, text: str, token: Token):
        raise ParserError(text, token)

    def next_token(self):
        return self.tokenizer.next()

    def next_token_b(self):
        token = self.next_token()
        self.back_token(token)
        return token

    def back_token(self, token: Token):
        self.tokenizer.back_token(token)

    def back_tokens(self, tokens: []):
        for token in tokens:
            self.back_token(token)

    def convert_token_param(self, t_type, t_value=None):
        t_value = t_value if isinstance(t_value, list) else [t_value]
        t_type = t_type if isinstance(t_type, list) else [t_type]
        return t_type, t_value

    def check_token(self, token, t_type, t_value=None):
        t_type, t_value = self.convert_token_param(t_type, t_value)
        return token.type in t_type and (t_value == [None] or token.value in t_value)

    def require(self, t_type, t_value=None):
        token = self.next_token()
        if not self.check_token(token, t_type, t_value):
            t_type, t_value = self.convert_token_param(t_type, t_value)
            self.error(ErrorType.EXPECTED.info(t_type if t_value == [None] else t_value), token)
        return token

    def compilation_unit(self):
        package_node = self.package_statement()
        import_list = []
        while self.check_token(self.next_token_b(), TokenType.KEY_WORD, KeyWordType.IMPORT):
            import_list.append(self.import_statement())
        import_node = NodeImport(import_list) if import_list else NodeNone()
        type_node = self.type_declaration() if not self.check_token(self.next_token_b(), TokenType.EOF) else NodeNone()
        return NodeCompUnit(package_node, import_node, type_node)

    def package_statement(self):
        self.require(TokenType.KEY_WORD, KeyWordType.PACKAGE)
        package = self.package_name()
        self.require(TokenType.SEPARATOR, SepType.SEMI)
        return package

    def import_statement(self):
        self.require(TokenType.KEY_WORD, KeyWordType.IMPORT)
        node = self.package_name()
        if self.check_token(self.next_token_b(), TokenType.OPERATION, OpType.MUL):
            node.children.append(NodeIdent(self.require(TokenType.OPERATION, OpType.MUL)))
        self.require(TokenType.SEPARATOR, SepType.SEMI)
        return node

    def type_declaration(self):
        return self.class_declaration()

    def class_declaration(self):
        modifiers = self.get_modifiers()
        self.require(TokenType.KEY_WORD, KeyWordType.CLASS)
        name = NodeIdent(self.require(TokenType.IDENT))
        self.require(TokenType.SEPARATOR, SepType.L_CURLY)
        fields = self.get_fields()
        self.require(TokenType.SEPARATOR, SepType.R_CURLY)
        return NodeClass(modifiers, name, fields)

    def get_fields(self):
        block = [self.field_declaration()]
        if isinstance(block[0], NodeNone):
            return NodeBlock(block)
        self.require(TokenType.SEPARATOR, SepType.SEMI)
        while not self.check_token(self.next_token_b(), TokenType.SEPARATOR, SepType.R_CURLY):
            block.append(self.field_declaration())
            self.require(TokenType.SEPARATOR, SepType.SEMI)
        return NodeBlock(block)

    def is_type(self, token: Token):
        return self.check_token(token, TokenType.IDENT) or self.check_token(token, TokenType.KEY_WORD,
                                                                            [KeyWordType.INT, KeyWordType.DOUBLE,
                                                                             KeyWordType.CHAR, KeyWordType.BOOLEAN,
                                                                             KeyWordType.VOID])

    def field_declaration(self):
        modifiers = self.get_modifiers()
        t_1, t_2 = self.next_token(), self.next_token()
        if self.check_token(t_1, TokenType.IDENT) and self.check_token(t_2, TokenType.SEPARATOR, SepType.L_PARENT):
            pass
        elif self.is_type(t_1) and self.check_token(t_2, TokenType.IDENT):
            t_3 = self.next_token()
            if self.check_token(t_3, TokenType.SEPARATOR, SepType.L_PARENT):
                pass
            elif self.check_token(t_3, TokenType.OPERATION, OpType.ASSIGN):
                return NodeVar(modifiers, NodeIdent(t_1), NodeIdent(t_2), self.variable_initializer())
            elif self.check_token(t_3, TokenType.SEPARATOR, SepType.L_BRACKET):
                self.require(TokenType.SEPARATOR, SepType.R_BRACKET)
                self.require(TokenType.OPERATION, OpType.ASSIGN)
                return NodeVar(modifiers, NodeIdent(t_1), NodeIdent(t_2), self.variable_initializer())
            elif self.check_token(t_3, TokenType.SEPARATOR, SepType.SEMI):
                self.back_token(t_3)
                return NodeVar(modifiers, NodeIdent(t_1), NodeIdent(t_2), NodeNone())
        else:
            self.back_tokens([t_2, t_1])
            return NodeNone()

    def variable_initializer(self):
        token = self.next_token()
        if self.check_token(token, TokenType.SEPARATOR, SepType.L_CURLY):
            block = [self.variable_initializer()]
            while self.check_token(token := self.next_token(), TokenType.SEPARATOR, SepType.COMMA):
                block.append(self.variable_initializer())
            self.back_token(token)
            self.require(TokenType.SEPARATOR, SepType.R_CURLY)
            return NodeBlock(block)
        else:
            self.back_token(token)
            return self.expr()

    def statement_block(self):
        self.require(TokenType.SEPARATOR, SepType.L_CURLY)
        self.require(TokenType.SEPARATOR, SepType.R_CURLY)
        return NodeBlock([])

    def package_name(self):
        block = [self.identifier()]
        while (self.check_token(token := self.next_token(), TokenType.SEPARATOR, SepType.POINT) and
               self.check_token(token := self.next_token(), TokenType.IDENT)):
            self.back_token(token)
            block.append(self.identifier())
        self.back_token(token)
        return NodePack(block)

    def identifier(self):
        token = self.require(TokenType.IDENT)
        return NodeIdent(token)

    def parse(self):
        return self.compilation_unit()

    def expr(self):
        node = self.term()
        while self.check_token(token := self.next_token(), TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            node = NodeBinOp(token, node, self.term())
        self.back_token(token)
        return node

    def term(self):
        node = self.factor()
        while self.check_token(token := self.next_token(), TokenType.OPERATION, [OpType.MUL, OpType.DIV]):
            node = NodeBinOp(token, node, self.factor())
        self.back_token(token)
        return node

    def factor(self):
        token = self.tokenizer.next()
        if self.check_token(token, TokenType.OPERATION, [OpType.PLUS, OpType.MINUS]):
            return NodeUnaryOp(token, self.factor())
        elif self.check_token(token, [TokenType.INT, TokenType.DOUBLE]):
            return NodeLiteral(token)
        elif self.check_token(token, TokenType.IDENT):
            return NodeIdent(token)
        elif self.check_token(token, TokenType.SEPARATOR, SepType.L_PARENT):
            node = self.expr()
            self.require(TokenType.SEPARATOR, SepType.R_PARENT)
            return node
        else:
            self.error('expr required', token)
