from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType, KeyWordType
from Main.genastdot import AstVizGen
from Parser.parser_ import Parser
from Tester.tester import LexTester, ParsTester, ExprTester


def test_lexer():
    LexTester().start_tests('../Tester/tests/lexer/', 10)


def test_expr():
    ExprTester().start_tests('../Tester/tests/expr/', 10)


class Main:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path).read()

    def calculate(self):
        tokenizer = Tokenizer(self.file)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        print(interpreter.calc())

    def print_ast(self):
        tokenizer = Tokenizer(self.file)
        parser = Parser(tokenizer)
        tree = parser.parse()
        AstVizGen(tree).generate()

    def print_tokens(self):
        tokenizer = Tokenizer(self.file)
        while (token := tokenizer.next()).type != TokenType.EOF:
            print(token)


if __name__ == '__main__':
    # test_expr()
    Main('test.java').print_ast()
