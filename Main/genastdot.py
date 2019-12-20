from graphviz import Source

from Parser.ast import NodeLiteral, NodeUnaryOp, NodeBinOp, NodeBlock, NodeIdent


class AstVizGen:
    def __init__(self, tree):
        self.tree = tree
        self.ncount = 1
        self.dot_header = ['digraph astgraph {',
                           '    node [shape=circle, fontsize=12, fontname="Courier", height=.1];',
                           '    ranksep=.3;',
                           '    edge [arrowsize=.5]']
        self.dot_body = []
        self.dot_footer = ['}']

    def visit(self, node):
        if isinstance(node, NodeLiteral) or isinstance(node, NodeIdent):
            s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
        elif isinstance(node, NodeUnaryOp):
            s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            self.visit(node.arg)
            s = '  node{} -> node{}\n'.format(node._num, node.arg._num)
            self.dot_body.append(s)
        elif isinstance(node, NodeBlock):
            s = '  node{} [label="block"]\n'.format(self.ncount)
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            for child in node.children:
                self.visit(child)
                s = '  node{} -> node{}\n'.format(node._num, child._num)
                self.dot_body.append(s)
        elif isinstance(node, NodeBinOp):
            s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            self.visit(node.left)
            s = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.dot_body.append(s)
            self.visit(node.right)
            s = '  node{} -> node{}\n'.format(node._num, node.right._num)
            self.dot_body.append(s)
        else:
            print('NOT FOUND')

    def gendot(self):
        self.visit(self.tree)
        content = ''.join(self.dot_header + self.dot_body + self.dot_footer)
        dot = Source(content, 'ast', format='png')
        dot.view(cleanup=True)
