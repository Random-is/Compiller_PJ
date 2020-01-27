from dataclasses import dataclass

from Parser.type import Type


@dataclass
class Symbol:
    name: str


@dataclass
class ClassSymbol(Symbol):
    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"


@dataclass
class VarSymbol(Symbol):
    type_: Type

    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', type='{self.type_}')>"


@dataclass
class MethodSymbol(Symbol):
    return_type: Type
    params: list

    def __str__(self):
        return f'<{self.__class__.__name__}(name={self.name}, type={self.return_type} parameters={self.params})>'

DEBUG = False

class ScopedSymbolTable:
    def __init__(self, name: str, level: int, enclosing_scope=None, method: MethodSymbol = None):
        # self.method = method
        self.symbols = {}
        self.name = name
        self.level = level
        self.enclosing_scope = enclosing_scope

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Scope name', self.name),
                ('Scope level', self.level),
                ('Enclosing scope',
                 self.enclosing_scope.name if self.enclosing_scope else None
                 )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %s' % (key, str(value)))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    @staticmethod
    def log(message):
        if DEBUG:
            print(message)

    def insert(self, symbol: Symbol):
        self.log(f'Insert: {symbol.name}')
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str, current_scope_only=False):
        self.log(f'Lookup: {name}. (Scope name: {self.name})')
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only:
            return symbol
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
