from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType, KeyWordType
from Main.genastdot import AstVizGen
from Parser.parser import Parser
from Parser.semantic_analyzer import SemanticAnalyzer
from Tester.tester import LexTester, ParsTester, ExprTester, SemanticsTester


class Main:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path).read()

    @staticmethod
    def test_lexer():
        LexTester().start_tests('../Tester/tests/lexer/', 30)

    @staticmethod
    def test_expr():
        ExprTester().start_tests('../Tester/tests/expr/', 10)

    @staticmethod
    def test_semantic():
        SemanticsTester().start_tests('../Tester/tests/semantic/', 5)

    @staticmethod
    def test_parser():
        ParsTester().start_tests('../Tester/tests/parser/', 20)

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

    def check_semantic(self):
        tokenizer = Tokenizer(self.file)
        parser = Parser(tokenizer)
        semantic = SemanticAnalyzer(parser, True)
        semantic.analyze()

    def print_tokens(self):
        tokenizer = Tokenizer(self.file)
        while (token := tokenizer.next()).type != TokenType.EOF:
            print(token)


if __name__ == '__main__':
    # test_expr()
    Main('test.java').test_parser()
