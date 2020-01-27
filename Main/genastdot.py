from enum import Enum

from graphviz import Source

from Parser.ast import Node, NodeNone
from Parser.type import *


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
        variables = node.__dict__
        if isinstance(node, Enum):
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name[name.index(".") + 1:]}"]\n'
        elif 'token' in variables:
            s = self.pref + f'node{self.ncount} [label="{node.token.raw_value}"]\n'
        elif issubclass(node.__class__, Node):
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name[4:]}"]\n'
        elif isinstance(node, (Class, Primitive)):
            s = self.pref + f'node{self.ncount} [label="{node.name}"]\n'
        elif isinstance(node, Array):
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name}"]\n'
        else:
            name = node.__class__.__name__
            s = self.pref + f'node{self.ncount} [label="{name}"]\n'
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        for key, value in variables.items():
            if isinstance(value, list):
                for x in value:
                    self.visit_(x)
                    s = self.pref + f'node{node._num} -> node{x._num}[label={key}]\n'
                    self.dot_body.append(s)
            elif isinstance(value, Node):
                self.visit_(value)
                s = self.pref + f'node{node._num} -> node{value._num}[label={key}]\n'
                self.dot_body.append(s)
            elif isinstance(value, (Class, Primitive)):
                self.visit_(value)
                s = self.pref + f'node{node._num} -> node{value._num}[label={key}]\n'
                self.dot_body.append(s)
            elif isinstance(value, Array):
                self.visit_(value)
                s = self.pref + f'node{node._num} -> node{value._num}[label={key}]\n'
                self.dot_body.append(s)

    def return_str_tree(self):
        self.visit_(self.tree)
        content = ''.join(self.dot_header + self.dot_body + self.dot_footer)
        return content

    def generate(self):
        self.visit_(self.tree)
        content = ''.join(self.dot_header + self.dot_body + self.dot_footer)
        # print(content)
        dot = Source(content, 'ast', format='png')
        dot.view(cleanup=True)
        # dot.render(cleanup=True)
