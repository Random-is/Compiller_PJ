from dataclasses import dataclass

from Lexer.token import Token


@dataclass
class Node:
    pass


@dataclass
class NodeWithToken(Node):
    token: Token


@dataclass
class NodeLiteral(NodeWithToken):
    pass


@dataclass
class NodeIdent(NodeWithToken):
    pass


@dataclass
class NodeKeyWord(NodeWithToken):
    pass


@dataclass
class NodeBinOp(NodeWithToken):
    left: Node
    right: Node


@dataclass
class NodeUnaryOp(NodeWithToken):
    arg: Node


@dataclass
class NodeBlock(Node):
    children: []


@dataclass
class NodeMod(NodeBlock):
    pass


@dataclass
class NodeClass(Node):
    name: NodeIdent
    fields: Node


@dataclass
class NodeCompUnit(Node):
    type_node: NodeClass


@dataclass
class NodeVar(Node):
    type: Node
    name: NodeIdent
    value: Node


@dataclass
class NodeMethod(Node):
    type: Node
    name: NodeIdent
    params: NodeBlock
    statements: NodeBlock


@dataclass
class NodeConstr(Node):
    name: NodeIdent
    params: NodeBlock
    statements: NodeBlock


@dataclass
class NodeNone(Node):
    pass
