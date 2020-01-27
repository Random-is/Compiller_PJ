from dataclasses import dataclass
from typing import Any


@dataclass
class Type:
    def_value: Any


@dataclass
class Array(Type):
    type_: Type

    def __str__(self) -> str:
        return f'{self.type_}[]'


@dataclass
class Class(Type):
    name: str

    def __str__(self) -> str:
        return f'Class {self.name}'


@dataclass
class Primitive(Type):
    name: str

    def __str__(self) -> str:
        return f'{self.name}'


@dataclass
class Void(Type):
    pass
