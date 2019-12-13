from Lexer.table import table_str
from Lexer.types import StateType, TokenType
from Lexer.token import Token


class Tokenizer:
    temp = ''
    symbol = ''
    state_dict = {}
    last_token = None
    pointer, line, last_nl = 0, 1, 0
    active_state = StateType.START
    keywords = ('import', 'class', 'public', 'static',
                'void', 'String', 'int', 'double', 'char', 'boolean',
                'return', 'break',
                'new', 'this',
                'if', 'else',
                'null', 'EOF')

    def __init__(self, file):
        self.file = file.read() + ' '
        self.file_len = len(self.file)
        self.generate_dict()

    def generate_dict(self):
        symbols = [chr(9), chr(10)] + [chr(i) for i in range(32, 127)]
        for i, state in enumerate((state for state in StateType)):
            for j, symbol in enumerate(symbols):
                self.state_dict.setdefault(state, {})[symbol] = self.state_table[i][j]

    # region Utility
    def new_line(self):
        self.last_nl = self.pointer
        self.line += 1
        return None

    def reset_state(self):
        self.active_state = StateType.START
        self.temp = ''
        return None

    def pointer_back(self):
        self.pointer -= 1
        return None

    def add_sym(self):
        self.temp += self.symbol
        return None

    def nt(self):
        return None

    # endregion

    # region Get Tokens
    def g_t_sep(self):
        self.temp += self.symbol
        return Token(self.temp, TokenType.SEPARATOR, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_sep_b(self):
        self.pointer_back()
        return Token(self.temp, TokenType.SEPARATOR, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_op(self):
        self.temp += self.symbol
        return Token(self.temp, TokenType.OPERATION, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_op_b(self):
        self.pointer_back()
        return Token(self.temp, TokenType.OPERATION, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_vv(self):
        self.temp += self.symbol
        return Token(self.temp, TokenType.VAR_VALUE, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_vv_b(self):
        self.pointer_back()
        return Token(self.temp, TokenType.VAR_VALUE, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_word(self):
        self.temp += self.symbol
        if self.temp in self.keywords:
            return Token(self.temp, TokenType.KEY_WORD, self.line, self.pointer - self.last_nl - len(self.temp) + 1)
        else:
            return Token(self.temp, TokenType.VAR_NAME, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def g_t_word_b(self):
        self.pointer_back()
        if self.temp in self.keywords:
            return Token(self.temp, TokenType.KEY_WORD, self.line, self.pointer - self.last_nl - len(self.temp) + 1)
        else:
            return Token(self.temp, TokenType.VAR_NAME, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    def err(self):
        self.temp += self.symbol
        return Token(self.temp, TokenType.EXCEPTION, self.line, self.pointer - self.last_nl - len(self.temp) + 1)

    # endregion

    # region States
    def less_s(self):
        self.active_state = StateType.LESS
        self.temp += self.symbol
        return None

    def more_s(self):
        self.active_state = StateType.MORE
        self.temp += self.symbol
        return None

    def not_s(self):
        self.active_state = StateType.NOT
        self.temp += self.symbol
        return None

    def r_slash_s(self):
        self.active_state = StateType.R_SLASH
        self.temp += self.symbol
        return None

    def slash_s(self):
        self.active_state = StateType.SLASH
        self.temp += self.symbol
        return None

    def comment_s(self):
        self.active_state = StateType.COMMENT
        self.temp = '//'
        return None

    def string_s(self):
        self.active_state = StateType.STRING
        self.temp += self.symbol
        return None

    def or_s(self):
        self.active_state = StateType.OR
        self.temp += self.symbol
        return None

    def and_s(self):
        self.active_state = StateType.AND
        self.temp += self.symbol
        return None

    def equals_s(self):
        self.active_state = StateType.EQUALS
        self.temp += self.symbol
        return None

    def minus_s(self):
        self.active_state = StateType.MINUS
        self.temp += self.symbol
        return None

    def zero_s(self):
        self.active_state = StateType.ZERO
        self.temp += self.symbol
        return None

    def int_s(self):
        self.active_state = StateType.INT
        self.temp += self.symbol
        return None

    def double_s(self):
        self.active_state = StateType.DOUBLE
        self.temp += self.symbol
        return None

    def word_s(self):
        self.active_state = StateType.WORD
        self.temp += self.symbol
        return None

    # endregion

    # region Other
    def end_string(self):
        # self.pointer += 1
        # return self.g_t_word_b()
        return self.g_t_vv()

    def end_r_slash(self):
        self.active_state = StateType.STRING
        self.temp += self.symbol
        return None

    def end_comment(self):
        return self.g_t_word_b()

    # endregion

    state_table = eval(table_str)

    def back_token(self, token):
        self.last_token = token

    def next(self):
        if self.last_token:
            token = self.last_token
            self.last_token = None
            return token
        while self.pointer < self.file_len:
            self.symbol = self.file[self.pointer]
            self.pointer += 1
            if token := self.state_dict[self.active_state][self.symbol](self):
                self.reset_state()
                return token
        return Token('EOF', TokenType.EOF, 0, 0)
