from Parser.ast import NodeBinOp, NodeLiteral


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        if isinstance(node, NodeLiteral):
            return int(node.token.value)
        elif isinstance(node, NodeBinOp):
            if node.token.value == "+":
                return self.visit(node.left) + self.visit(node.right)
            elif node.token.value == "-":
                return self.visit(node.left) - self.visit(node.right)
            elif node.token.value == "*":
                return self.visit(node.left) * self.visit(node.right)
            elif node.token.value == "/":
                return self.visit(node.left) / self.visit(node.right)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
