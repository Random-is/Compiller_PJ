from dataclasses import dataclass
from typing import Any

from lexer.token import Token


@dataclass
class Node:
    token: Token


@dataclass
class NodeLiteral(Node):
    value = 0


@dataclass
class NodeIdent(Node):
    name: str


@dataclass
class NodeKeyword(Node):
    pass


@dataclass
class NodeBinOp(Node):
    op: Any
    left: Node
    right: Node


@dataclass
class NodeUnaryOp(Node):
    op: Any
    arg: Node
