from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType
from Main.tree_printer import PrintNode
from Parser.parser import Parser
from Tester.tester import LexTester, ParsTester


def test_lexer():
    LexTester().start_tests('../Tester/tests/lexer/', 10)


def test_parser():
    ParsTester().start_tests('../Tester/tests/parser/', 10)


class Main:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path)

    def calculate(self):
        tokenizer = Tokenizer(file=self.file)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        print(interpreter.interpret())

    def print_ast(self):
        tokenizer = Tokenizer(file=self.file)
        parser = Parser(tokenizer)
        tree = parser.parse()
        print(PrintNode(tree=tree).get_tree())

    def print_tokens(self):
        tokenizer = Tokenizer(self.file)
        while (token := tokenizer.next()).type != TokenType.EOF:
            print(token)


if __name__ == '__main__':
    # test_parser()
    Main('../Tester/tests/lexer/file4.java').print_ast()
