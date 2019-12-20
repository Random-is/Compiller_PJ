from Parser.ast import NodeBinOp, NodeLiteral, NodeUnaryOp


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        if isinstance(node, NodeLiteral):
            return eval(node.token.value)
        elif isinstance(node, NodeUnaryOp):
            return -self.visit(node.arg)
        elif isinstance(node, NodeBinOp):
            if node.token.value == "+":
                return self.visit(node.left) + self.visit(node.right)
            elif node.token.value == "-":
                return self.visit(node.left) - self.visit(node.right)
            elif node.token.value == "*":
                return self.visit(node.left) * self.visit(node.right)
            elif node.token.value == "/":
                return self.visit(node.left) / self.visit(node.right)

    def calc(self):
        tree = self.parser.expr()
        return self.visit(tree)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
