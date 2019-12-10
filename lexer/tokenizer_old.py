from lexer.token import Token
from lexer.types import TokenType


def is_int(lex):
    return lex.isdigit()


def is_double(lex):
    return lex.replace('.', '').isnumeric()


def is_string(lex):
    return lex.count('"') - lex.count('\\"') == 2


def is_boolean(lex):
    return lex in ['true', 'false']


def is_not_start_string(lex):
    return lex.count('"') == 0 or is_string(lex)


def is_separator(lex):
    return lex in [';', '{', '}', '(', ')', '[', ']'] or (lex[-1] == '.' and not lex[0].isdigit())


def is_spacer(lex):
    return lex in [' ', '\n']


def is_operation(lex):
    return lex in ['=', '+', '-', '/', '*', '&', '&&', '|', '||', '==', '->']


def is_key_word(lex):
    return lex in ['import', 'class', 'public', 'static', 'void', 'return',
                   'new', 'this', 'String', 'int', 'double', 'char', 'if',
                   'then', 'else', 'break', 'null', 'EOF']


class Tokenizer(object):
    def __init__(self, file):
        self.file = file.read() + '\nEOF '
        self.pointer = 0
        self.line = 1
        self.last_nl = 0

    def next(self):
        temp = ''
        while self.pointer < len(self.file):
            if self.file[self.pointer] == '\n':
                self.line += 1
                self.last_nl = self.pointer + 1
            temp += self.file[self.pointer]
            if is_spacer(temp):
                temp = ''
            if (temp
                    and is_not_start_string(temp)
                    and (is_separator(self.file[self.pointer])
                         or is_spacer(self.file[self.pointer]))):
                if len(temp) == 1:
                    self.pointer += 1
                else:
                    temp = temp[0:-1]
                if is_separator(temp):
                    return Token(temp, TokenType.SEPARATOR, self.line, self.pointer - self.last_nl - len(temp) + 1)
                elif is_operation(temp):
                    return Token(temp, TokenType.OPERATION, self.line, self.pointer - self.last_nl - len(temp) + 1)
                elif is_int(temp) or is_double(temp) or is_string(temp) or is_boolean(temp):
                    return Token(temp, TokenType.VAR_VALUE, self.line, self.pointer - self.last_nl - len(temp) + 1)
                elif is_key_word(temp):
                    return Token(temp, TokenType.KEY_WORD, self.line, self.pointer - self.last_nl - len(temp) + 1)
                else:
                    return Token(temp, TokenType.VAR_NAME, self.line, self.pointer - self.last_nl - len(temp) + 1)
            self.pointer += 1
