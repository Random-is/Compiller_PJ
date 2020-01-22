from Lexer.table import table_str
from Lexer.types import StateType, TokenType, KeyWordType, SepType, OpType, BoolType
from Lexer.token import Token
from Main.error import LexerError, ErrorType


class Tokenizer:

    def __init__(self, text: str):
        self.text = text + '\n'
        self.file_len = len(self.text)
        self.last_tokens = []
        self.temp = self.symbol = ''
        self.active_state = StateType.START
        self.pointer, self.line, self.last_nl = 0, 1, 0
        self.state_dict = self.generate_dict(eval(table_str))
        self.booleans = tuple(x.value for x in BoolType)
        self.keywords = tuple(x.value for x in KeyWordType)

    @staticmethod
    def generate_dict(state_table):
        result = {}
        symbols = [chr(9), chr(10)] + [chr(i) for i in range(32, 127)]
        for i, state in enumerate((state for state in StateType)):
            for j, symbol in enumerate(symbols):
                result.setdefault(state, {})[symbol] = state_table[i][j]
        return result

    # region Utility
    @staticmethod
    def nt():
        return None

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

    def get_pos(self):
        return self.pointer - self.last_nl - len(self.temp) + 1

    def check_word(self):
        if self.temp in self.booleans:
            return Token(BoolType(self.temp), self.temp, TokenType.KEY_WORD, self.line, self.get_pos())
        elif self.temp in self.keywords:
            return Token(KeyWordType(self.temp), self.temp, TokenType.KEY_WORD, self.line, self.get_pos())
        else:
            return Token(self.temp, self.temp, TokenType.IDENT, self.line, self.get_pos())

    # endregion

    # region Get Tokens
    def g_t_sep(self):
        self.temp += self.symbol
        return Token(SepType(self.temp), self.temp, TokenType.SEPARATOR, self.line, self.get_pos())

    def g_t_sep_b(self):
        self.pointer_back()
        return Token(SepType(self.temp), self.temp, TokenType.SEPARATOR, self.line, self.get_pos())

    def g_t_op(self):
        self.temp += self.symbol
        return Token(OpType(self.temp), self.temp, TokenType.OPERATION, self.line, self.get_pos())

    def g_t_op_b(self):
        self.pointer_back()
        return Token(OpType(self.temp), self.temp, TokenType.OPERATION, self.line, self.get_pos())

    def g_t_int_b(self):
        self.pointer_back()
        return Token(int(self.temp), self.temp, TokenType.INT, self.line, self.get_pos())

    def g_t_dbl(self):
        self.temp += self.symbol
        return Token(float(self.temp), self.temp, TokenType.DOUBLE, self.line, self.get_pos())

    def g_t_dbl_b(self):
        self.pointer_back()
        return Token(float(self.temp), self.temp, TokenType.DOUBLE, self.line, self.get_pos())

    def g_t_char(self):
        self.temp += self.symbol
        return Token(self.temp[1:-1], self.temp, TokenType.CHAR, self.line, self.get_pos())

    def g_t_str(self):
        self.temp += self.symbol
        return Token(self.temp[1:-1], self.temp, TokenType.STRING, self.line, self.get_pos())

    def g_t_word_b(self):
        self.pointer_back()
        return self.check_word()

    def err(self):
        self.temp += self.symbol
        token = Token(self.temp, self.temp, TokenType.EXCEPTION, self.line, self.get_pos())
        raise LexerError(ErrorType.UNEXPECTED_TOKEN.value, token)

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

    def r_s_char_s(self):
        self.active_state = StateType.R_SLASH_CHAR
        self.temp += self.symbol
        return None

    def r_s_str_s(self):
        self.active_state = StateType.R_SLASH_STR
        self.temp += self.symbol
        return None

    def slash_s(self):
        self.active_state = StateType.SLASH
        self.temp += self.symbol
        return None

    def comment_s(self):
        self.active_state = StateType.COMMENT
        self.temp += self.symbol
        return None

    def string_s(self):
        self.active_state = StateType.STRING
        self.temp += self.symbol
        return None

    def char_s(self):
        self.active_state = StateType.CHAR
        self.temp += self.symbol
        return None

    def e_char_s(self):
        self.active_state = StateType.END_CHAR
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
    def end_r_s_str(self):
        self.active_state = StateType.STRING
        self.temp += self.symbol
        return None

    def end_r_s_char(self):
        self.active_state = StateType.END_CHAR
        self.temp += self.symbol
        return None

    def end_comment(self):
        self.pointer_back()
        self.reset_state()
        return None

    # endregion

    def back_token(self, *token: Token):
        for t in token:
            self.last_tokens.append(t)

    def next_back(self):
        token = self.next()
        self.back_token(token)
        return token

    def next(self):
        if self.last_tokens:
            return self.last_tokens.pop()
        while self.pointer < self.file_len:
            self.symbol = self.text[self.pointer]
            self.pointer += 1
            if (token := self.state_dict[self.active_state][self.symbol]()) is not None:
                self.reset_state()
                return token
        return Token('', '', TokenType.EOF, 0, 0)
