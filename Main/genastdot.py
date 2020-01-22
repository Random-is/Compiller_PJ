from enum import Enum

from graphviz import Source

from Parser.ast import Node


class AstVizGen:
    def __init__(self, tree):
        self.tree = tree
        self.ncount = 1
        self.pref = ' ' * 2
        self.dot_header = ['digraph astgraph {\n',
                           '  node [shape=circle, fontsize=12, fontname="Courier", height=.1];\n',
                           '  ranksep=.3;\n',
                           '  edge [arrowsize=.5]\n']
        self.dot_body = []
        self.dot_footer = ['}']

    def visit_(self, node):
        s = ''
        variables = node.__dict__
        if isinstance(node, Enum):
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name[name.index(".") + 1:]}"]\n'
        elif 'token' in variables:
            s = self.pref + f'node{self.ncount} [label="{node.token.raw_value}"]\n'
        elif issubclass(node.__class__, Node):
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name[4:]}"]\n'
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        for key, value in variables.items():
            if key not in ['token', '_num']:
                if isinstance(value, list):
                    for x in value:
                        self.visit_(x)
                        s = self.pref + f'node{node._num} -> node{x._num}[label={key}]\n'
                        self.dot_body.append(s)
                else:
                    self.visit_(value)
                    s = self.pref + f'node{node._num} -> node{value._num}[label={key}]\n'
                    self.dot_body.append(s)

    def generate(self):
        self.visit_(self.tree)
        content = ''.join(self.dot_header + self.dot_body + self.dot_footer)
        # print(content)
        dot = Source(content, 'ast', format='png')
        dot.view(cleanup=True)
        # dot.render(cleanup=True)
