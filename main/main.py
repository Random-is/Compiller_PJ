from lexer.tokenizer import Tokenizer


class Main(object):
    def __init__(self, path):
        self.path = path

    def compile(self):
        file = open(self.path)
        tokenizer = Tokenizer(file)
        while (token := tokenizer.next()).value != 'EOF':
            print(token)
            pass


# start_time = time.time()
Main('../assets/file1.java').compile()
# print("--- %s seconds ---" % (time.time() - start_time))
