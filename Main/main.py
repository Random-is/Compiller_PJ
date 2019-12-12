from Interpreter.interpreter import Interpreter
from Lexer.tokenizer import Tokenizer
from Parser.parser import Parser


class Main:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path)

    def print_ast(self):
        tokenizer = Tokenizer(self.file)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        return interpreter.interpret()

    def print_tokens(self):
        tokenizer = Tokenizer(self.file)
        while (token := tokenizer.next()).value != 'EOF':
            print(token)


if __name__ == '__main__':
    # Main('../Testers/lex_tester/tests/file1.java').print_tokens()
    print(Main('../Testers/lex_tester/tests/file4.java').print_ast())
