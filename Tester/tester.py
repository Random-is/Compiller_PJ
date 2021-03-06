from termcolor import colored

from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Lexer.types import TokenType
from Main.error import Error
from Main.genastdot import AstVizGen
from Parser.parser import Parser
from Parser.semantic_analyzer import SemanticAnalyzer


class Tester:
    @staticmethod
    def parse_test(file_path):
        test = answer = ''
        file = open(file_path)
        lines = file.readlines()
        while (line := lines.pop(0)) != "EOF\n":
            test += line
        for line in lines:
            answer += line
        return test[:-1], answer

    def get_result(self, test):
        pass

    def start_tests(self, test_path, test_count):
        for i in range(test_count):
            file_path = test_path + '{:0>3}.java'.format(i + 1)
            test, answer = self.parse_test(file_path)
            result = self.get_result(test)


            new_test = open(file_path, 'w')
            new_test.write(test + '\nEOF\n' + result)


            if answer != result:
                print('{0}\n{1}\n{2}'.format(test, answer, result))
            print('test {0:3} -> {1}'.format(i + 1, colored(answer == result, 'green' if answer == result else 'red')))


class LexTester(Tester):
    def get_result(self, test):
        result = ''
        tokenizer = Tokenizer(text=test)
        try:
            while (token := tokenizer.next()).type != TokenType.EOF:
                result += str(token) + '\n'
            return result[:-1]
        except Error as e:
            return e.message


class ParsTester(Tester):
    def get_result(self, test):
        tokenizer = Tokenizer(text=test)
        parser = Parser(tokenizer)
        try:
            tree = parser.parse()
            return AstVizGen(tree).return_str_tree()
        except Error as e:
            return e.message


class ExprTester(Tester):
    def get_result(self, test):
        tokenizer = Tokenizer(text=test)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        try:
            res = str(interpreter.calc())
            return res
        except Error as e:
            return e.message


class SemanticsTester(Tester):
    def get_result(self, test):
        tokenizer = Tokenizer(text=test)
        parser = Parser(tokenizer)
        semantics = SemanticAnalyzer(parser, False)
        try:
            semantics.analyze()
        except Error as e:
            return e.message
