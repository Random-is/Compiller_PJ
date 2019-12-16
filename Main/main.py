from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType
from Parser.parser import Parser
from Tester.tester import LexTester, ParsTester


def test_lexer():
    LexTester().start_tests('../Tester/tests/lexer/', 10)


def test_parser():
    ParsTester().start_tests('../Tester/tests/parser/', 10)


class Main:
    def __init__(self, path=None):
        if path:
            self.path = path
            self.file = open(self.path)

    def print_ast(self):
        tokenizer = Tokenizer(file=self.file)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        print(interpreter.interpret())

    def print_tokens(self):
        tokenizer = Tokenizer(self.file)
        while (token := tokenizer.next()).type != TokenType.EOF:
            print(token)


if __name__ == '__main__':
    test_parser()
    # Main('../Tester/lex_tester/tests/file4.java').print_tokens()

