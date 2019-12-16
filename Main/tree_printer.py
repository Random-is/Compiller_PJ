from Parser.ast import NodeLiteral, NodeUnaryOp, NodeBinOp


class PrintNode:
    def __init__(self, tree=None, value=None, left=None, right=None):
        if tree:
            def visit(node):
                if isinstance(node, NodeLiteral):
                    return PrintNode(value=node.token.value)
                elif isinstance(node, NodeUnaryOp):
                    return PrintNode(value=node.token.value, left=visit(node.arg))
                elif isinstance(node, NodeBinOp):
                    return PrintNode(value=node.token.value, left=visit(node.left), right=visit(node.right))
            tree = visit(tree)
            self.value = tree.value
            self.right = tree.right
            self.left = tree.left
        else:
            self.value = value
            self.right = right
            self.left = left

    def get_tree(self):
        lines, _, _, _ = self._display_aux()
        return '\n'.join(lines)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        value = '({})'.format(self.value)
        # No child.
        if self.right is None and self.left is None:
            line = value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle
        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2
        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2