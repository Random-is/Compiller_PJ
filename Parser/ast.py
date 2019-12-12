from dataclasses import dataclass

from Lexer.token import Token


@dataclass
class Node:
    token: Token


@dataclass
class NodeLiteral(Node):
    pass


@dataclass
class NodeIdent(Node):
    pass


@dataclass
class NodeKeyword(Node):
    pass


@dataclass
class NodeBinOp(Node):
    left: Node
    right: Node


@dataclass
class NodeUnaryOp(Node):
    arg: Node
