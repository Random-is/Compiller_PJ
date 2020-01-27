from Lexer.token import Token
from Main.error import SemanticError, ErrorType
from Parser.ast import *
from Parser.parser import Parser, OpType, TokenType, KeyWordType
from Parser.symbol_table import ScopedSymbolTable, ClassSymbol, VarSymbol, MethodSymbol
from Parser.type import Array, Primitive, Void


class SemanticAnalyzer:
    def __init__(self, parser: Parser, DEBUG: bool):
        self.DEBUG = DEBUG
        self.parser = parser
        self.current_scope: ScopedSymbolTable = None

    def analyze(self):
        tree = self.parser.parse()
        self.visit(tree)

    def log(self, message):
        if self.DEBUG:
            print(message)

    def error(self, text: str, token: Token):
        raise SemanticError(text, token)

    def visit(self, node: Node):
        if isinstance(node, NodeCompUnit):
            self.comp_unit(node)
        elif isinstance(node, NodeClass):
            self.class_(node)
        elif isinstance(node, NodeVar):
            self.var(node)
        elif isinstance(node, NodeBlock):
            self.block(node)
        elif isinstance(node, NodeLiteral):
            return self.literal(node)
        elif isinstance(node, NodeBinOp):
            return self.bin_op(node)
        elif isinstance(node, NodeUnaryOp):
            return self.unary_op(node)
        elif isinstance(node, NodeNone):
            pass
        elif isinstance(node, NodeArrInit):
            return self.arr_init(node)
        elif isinstance(node, NodeMethod):
            self.method(node)
        elif isinstance(node, NodeAssign):
            self.assign(node)
        elif isinstance(node, NodeNewArr):
            return self.new_arr(node)
        elif isinstance(node, NodeArrItem):
            return self.arr_item(node)
        elif isinstance(node, NodeMCall):
            self.method_call(node)
        elif isinstance(node, NodeIdent):
            return self.ident(node)
        elif isinstance(node, NodeFor):
            self.for_(node)
        elif isinstance(node, NodeIf):
            self.if_(node)
        elif isinstance(node, NodeReturn):
            self.return_(node)

    def log_enter_scope(self, name: str):
        self.log(f'ENTER scope: {name}')

    def log_leave_scope(self, name: str):
        self.log(f'LEAVE scope: {name}')

    def block(self, node: NodeBlock):
        for item in node.children:
            self.visit(item)

    def arr_init(self, node: NodeArrInit):
        type_ = self.visit(node.children[0])
        for item in node.children:
            if type_ != self.visit(item):
                self.error('REQ SAME TYPES IN ARAY INIT', None)
        return type_





    def get_var_type(self, value: Token):
        if value.type == TokenType.CHAR:
            return self.parser.type_table[KeyWordType.CHAR.value]
        elif value.type == TokenType.STRING:
            return self.parser.type_table[KeyWordType.STRING.value]
        elif value.type == TokenType.INT:
            return self.parser.type_table[KeyWordType.INT.value]
        elif value.type == TokenType.DOUBLE:
            return self.parser.type_table[KeyWordType.DOUBLE.value]
        elif value.type == TokenType.BOOLEAN:
            return self.parser.type_table[KeyWordType.BOOLEAN.value]

    def literal(self, node: NodeLiteral):
        return self.get_var_type(node.token)

    def return_(self, node: NodeReturn):
        method = self.current_scope.method
        if not method:
            self.error('RETURN NOT IN METHOD', node.token)
        if isinstance(method.return_type, Void):
            self.error('NOT ALLOW RETURN IN VOID METHOD', node.token)
        if method.return_type != self.visit(node.expr):
            self.error('RETURN ' + str(method.return_type) + ' EXPECTED', node.token)

    def bin_op(self, node: NodeBinOp):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        op = node.token.value
        t = self.parser.type_table
        if op == OpType.PLUS:
            if ((type_left == t[KeyWordType.INT.value] or type_left == t[KeyWordType.DOUBLE.value]) and
                    (type_right == t[KeyWordType.INT.value] or type_right == t[KeyWordType.DOUBLE.value])):
                if type_left == t[KeyWordType.INT.value] and type_right == t[KeyWordType.INT.value]:
                    return t[KeyWordType.INT.value]
                else:
                    return t[KeyWordType.DOUBLE.value]
            elif ((type_left == t[KeyWordType.CHAR.value] or type_left == t[KeyWordType.STRING.value]) and
                    (type_right == t[KeyWordType.CHAR.value] or type_right == t[KeyWordType.STRING.value])):
                if type_left == t[KeyWordType.CHAR.value] and type_right == t[KeyWordType.CHAR.value]:
                    return t[KeyWordType.CHAR.value]
                else:
                    return t[KeyWordType.STRING.value]
            else:
                self.error('REQ NUMERIC or STRING expr', node.token)
        elif op == OpType.DIV or op == OpType.MOD or op == OpType.MUL or op == OpType.MINUS:
            if ((type_left == t[KeyWordType.INT.value] or type_left == t[KeyWordType.DOUBLE.value]) and
                    (type_right == t[KeyWordType.INT.value] or type_right == t[KeyWordType.DOUBLE.value])):
                if type_left == t[KeyWordType.INT.value] and type_right == t[KeyWordType.INT.value]:
                    return t[KeyWordType.INT.value]
                else:
                    return t[KeyWordType.DOUBLE.value]
            else:
                self.error('REQ NUMERIC expr', node.token)
        elif (op == OpType.EQUALS or op == OpType.NOT_EQUALS  or op == OpType.LESS or op == OpType.LESS_EQUALS or op == OpType.MORE or
                op == OpType.MORE_EQUALS):
            if type_left == type_right:
                return t[KeyWordType.BOOLEAN.value]
            else:
                self.error('REQ SAME TYPES TO COMPARE', node.token)
        elif op == OpType.OR or op == OpType.AND:
            if type_left == t[KeyWordType.BOOLEAN.value] and type_right == t[KeyWordType.BOOLEAN.value]:
                return type_left
            else:
                self.error('REQ BOOLEAN EXPR', node.token)

    def unary_op(self, node: NodeUnaryOp):
        arg = self.visit(node.arg)
        op = node.token.value
        t = self.parser.type_table
        if op == OpType.PLUS or op == OpType.MINUS:
            if arg == t[KeyWordType.INT.value] or arg == t[KeyWordType.DOUBLE.value]:
                return arg
            else:
                self.error('REQ NUMERIC EXPR', node.token)
        elif op == OpType.NOT:
            if arg == t[KeyWordType.BOOLEAN.value]:
                return arg
            else:
                self.error('REQ BOOLEAN EXPR', node.token)

    def comp_unit(self, node: NodeCompUnit):
        # name = node.__class__.__name__[4:]
        # self.log_enter_scope(name)
        scope = ScopedSymbolTable(name, 0)
        self.current_scope = scope
        self.visit(node.class_)
        # self.log(scope)
        self.log_leave_scope(name)

    def class_(self, node: NodeClass):
        class_name = node.name.token.raw_value
        class_symbol = ClassSymbol(class_name)
        self.current_scope.insert(class_symbol)
        name = f'{node.__class__.__name__[4:]}: {class_name}'
        self.log_enter_scope(name)
        scope = ScopedSymbolTable(name, self.current_scope.level + 1, self.current_scope)
        self.current_scope = scope
        self.visit(node.fields)
        self.log(scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log_leave_scope(name)

    def var(self, node: NodeVar):
        var_name = node.name.token.raw_value
        type_ = node.type_
        var_symbol = VarSymbol(var_name, type_)
        if self.current_scope.lookup(var_name, True):
            self.error(ErrorType.DUPLICATE_ID.value, node.name.token)
        if (init_type := self.visit(node.value)) is not None:
            if init_type != type_:
                self.error('REQUIRE ' + str(type_), node.name.token)
        self.current_scope.insert(var_symbol)

    def method(self, node: NodeMethod):
        method_name = node.name.token.raw_value
        type_ = node.type_
        params = [t.type_ for t in node.params.children]
        method_symbol = MethodSymbol(method_name, type_, params)
        if self.current_scope.lookup(method_name):
            self.error(ErrorType.DUPLICATE_ID.value, node.name.token)
        self.current_scope.insert(method_symbol)
        name = f'{node.__class__.__name__[4:]}: {method_name}'
        self.log_enter_scope(name)
        scope = ScopedSymbolTable(name, self.current_scope.level + 1, self.current_scope, method_symbol)
        self.current_scope = scope
        self.visit(node.params)
        self.visit(node.statements)
        self.log(scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log_leave_scope(name)

    def for_(self, node: NodeFor):
        name = 'For Scope'
        self.log_enter_scope(name)
        scope = ScopedSymbolTable(name, self.current_scope.level + 1, self.current_scope)
        self.current_scope = scope
        self.visit(node.for_init)
        if self.visit(node.expr) != self.parser.type_table[KeyWordType.BOOLEAN.value]:
            self.error('BOOLEAN EXPR EXPECTED', node.expr.token)
        self.visit(node.for_update)
        self.visit(node.statements)
        self.log(scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log_leave_scope(name)

    def if_(self, node: NodeIf):
        name = 'If Scope'
        self.log_enter_scope(name)
        scope = ScopedSymbolTable(name, self.current_scope.level + 1, self.current_scope)
        self.current_scope = scope
        if self.visit(node.expr) != self.parser.type_table[KeyWordType.BOOLEAN.value]:
            self.error('BOOLEAN EXPR EXPECTED', node.expr.token)
        self.visit(node.statements)
        self.visit(node.else_statements)
        self.log(scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log_leave_scope(name)


    def method_call(self, node: NodeMCall):
        method_name = node.name.value
        arguments = node.arguments
        method_symbol = self.current_scope.lookup(method_name)
        if method_symbol is None or not isinstance(method_symbol, MethodSymbol):
            self.error('METHOD ID NOT FOUND', node.name.token)
        for i, arg_type in enumerate(method_symbol.params):
            if self.visit(arguments.children[i]) != arg_type:
                self.error('REQ ' + str(arg_type) + ' ARG TYPE', arguments.children[i].token)

    def ident(self, node: NodeIdent):
        name = node.token.value
        ident_symbol = self.current_scope.lookup(name)
        if ident_symbol is None or not isinstance(ident_symbol, VarSymbol):
            self.error('VAR ID NOT FOUND', node.token)
        print(ident_symbol.type_)
        return ident_symbol.type_

    def get_arr_size(self, type_: Array):
        n = 0
        while not isinstance(type_, Primitive):
            type_ = type_.type_
            n += 1
        return n

    def get_arr_item_type(self, type_: Type, count: int):
        for i in range(count):
            type_ = type_.type_
        return type_

    def assign(self, node: NodeAssign):
        expr = node.expr
        print(node.var_name)
        var_type = self.visit(node.var_name)
        print(var_type)
        if var_type != self.visit(expr):
            self.error('REQ ' + str(var_type) + ' TYPE', node.token)

    def arr_item(self, node: NodeArrItem):
        mas_name = node.token.value
        indexes = node.indexes
        mas_symbol = self.current_scope.lookup(mas_name)
        if mas_symbol is None:
            self.error('VAR ID NOT FOUND', node.token)
        elif self.get_arr_size(mas_symbol.type_) >= len(indexes.children):
            for index_expr in indexes.children:
                if self.visit(index_expr) != self.parser.type_table[KeyWordType.INT.value]:
                    self.error('INT TYPE REQUIRED', index_expr)
            return self.get_arr_item_type(mas_symbol.type_, len(indexes.children))
        else:
            self.error('REQ ' + str(self.get_arr_size(mas_symbol.type_)) + ' MAS SIZE', node.token)

    def new_arr(self, node: NodeNewArr):
        for index_expr in node.lengths.children:
            if self.visit(index_expr) != self.parser.type_table[KeyWordType.INT.value]:
                self.error('INT TYPE REQUIRED', index_expr)
        return node.type_


    # def visit_Block(self, node):
    #     for declaration in node.declarations:
    #         self.visit(declaration)
    #     self.visit(node.compound_statement)
    #
    # def visit_Program(self, node):
    #     self.log('ENTER scope: global')
    #     global_scope = ScopedSymbolTable(
    #         scope_name='global',
    #         scope_level=1,
    #         enclosing_scope=self.current_scope,  # None
    #     )
    #     global_scope._init_builtins()
    #     self.current_scope = global_scope
    #
    #     # visit subtree
    #     self.visit(node.block)
    #
    #     self.log(global_scope)
    #
    #     self.current_scope = self.current_scope.enclosing_scope
    #     self.log('LEAVE scope: global')
    #
    # def visit_Compound(self, node):
    #     for child in node.children:
    #         self.visit(child)
    #
    # def visit_NoOp(self, node):
    #     pass
    #
    # def visit_BinOp(self, node):
    #     self.visit(node.left)
    #     self.visit(node.right)
    #
    # def visit_ProcedureDecl(self, node):
    #     proc_name = node.proc_name
    #     proc_symbol = ProcedureSymbol(proc_name)
    #     self.current_scope.insert(proc_symbol)
    #
    #     self.log(f'ENTER scope: {proc_name}')
    #     # Scope for parameters and local variables
    #     procedure_scope = ScopedSymbolTable(
    #         scope_name=proc_name,
    #         scope_level=self.current_scope.scope_level + 1,
    #         enclosing_scope=self.current_scope
    #     )
    #     self.current_scope = procedure_scope
    #
    #     # Insert parameters into the procedure scope
    #     for param in node.params:
    #         param_type = self.current_scope.lookup(param.type_node.value)
    #         param_name = param.var_node.value
    #         var_symbol = VarSymbol(param_name, param_type)
    #         self.current_scope.insert(var_symbol)
    #         proc_symbol.params.append(var_symbol)
    #
    #     self.visit(node.block_node)
    #
    #     self.log(procedure_scope)
    #
    #     self.current_scope = self.current_scope.enclosing_scope
    #     self.log(f'LEAVE scope: {proc_name}')
    #
    # def visit_VarDecl(self, node):
    #     type_name = node.type_node.value
    #     type_symbol = self.current_scope.lookup(type_name)
    #
    #     # We have all the information we need to create a variable symbol.
    #     # Create the symbol and insert it into the symbol table.
    #     var_name = node.var_node.value
    #     var_symbol = VarSymbol(var_name, type_symbol)
    #
    #     # Signal an error if the table already has a symbol
    #     # with the same name
    #     if self.current_scope.lookup(var_name, current_scope_only=True):
    #         self.error(
    #             error_code=ErrorCode.DUPLICATE_ID,
    #             token=node.var_node.token,
    #         )
    #
    #     self.current_scope.insert(var_symbol)
    #
    # def visit_Assign(self, node):
    #     # right-hand side
    #     self.visit(node.right)
    #     # left-hand side
    #     self.visit(node.left)
    #
    # def visit_Var(self, node):
    #     var_name = node.value
    #     var_symbol = self.current_scope.lookup(var_name)
    #     if var_symbol is None:
    #         self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token)
    #
    # def visit_Num(self, node):
    #     pass
    #
    # def visit_UnaryOp(self, node):
    #     pass
    #
    # def visit_ProcedureCall(self, node):
    #     for param_node in node.actual_params:
    #         self.visit(param_node)
