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
class NodePack(NodeBlock):
    pass


@dataclass
class NodeImport(NodeBlock):
    pass


@dataclass
class NodeModifier(NodeBlock):
    pass


@dataclass
class NodeMod(NodeBlock):
    pass


@dataclass
class NodeCompUnit(Node):
    package_node: NodePack
    import_node: Node
    type_node: Node


@dataclass
class NodeClass(Node):
    modifiers: NodeMod
    name: NodeIdent
    fields: Node


@dataclass
class NodeVar(Node):
    modifiers: NodeMod
    type: Node
    name: NodeIdent
    value: Node


@dataclass
class NodeNone(Node):
    pass
