from dataclasses import dataclass
from typing import Any

from Lexer.token import Token
from Parser.type import Type


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
    children: list


@dataclass
class NodeMod(NodeBlock):
    pass


@dataclass
class NodeClass(Node):
    name: NodeIdent
    fields: Node


@dataclass
class NodeCompUnit(Node):
    class_: NodeClass


@dataclass
class NodeVar(Node):
    type_: Type
    name: NodeIdent
    value: Node


@dataclass
class NodeMethod(Node):
    type_: Type
    name: NodeIdent
    params: NodeBlock
    statements: NodeBlock


@dataclass
class NodeMCall(Node):
    name: NodeIdent
    arguments: NodeBlock


@dataclass
class NodeConstr(Node):
    name: NodeIdent
    params: NodeBlock
    statements: NodeBlock


@dataclass
class NodeAssign(NodeWithToken):
    var_name: NodeIdent
    expr: Node


@dataclass
class NodeNewArr(NodeWithToken):
    type_: Type
    lengths: NodeBlock


@dataclass
class NodeArrInit(NodeBlock):
    pass


@dataclass
class NodeArrItem(NodeWithToken):
    indexes: NodeBlock


@dataclass
class NodeReturn(NodeWithToken):
    expr: Node


@dataclass
class NodeIf(NodeWithToken):
    expr: NodeWithToken
    statements: NodeBlock
    else_statements: NodeBlock


@dataclass
class NodeFor(NodeWithToken):
    for_init: Node
    expr: NodeWithToken
    for_update: Node
    statements: NodeBlock


@dataclass
class NodeNone(Node):
    pass
