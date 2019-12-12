from termcolor import colored

from Lexer.tokenizer import Tokenizer


def get_answer(file_path):
    check = False
    answer = ''
    for line in open(file_path).readlines():
        if check:
            if line != '\n':
                answer += line
        if line == 'EOF\n':
            check = True
    return answer


def get_token_str(file_path):
    file = open(file_path)
    tokenizer = Tokenizer(file)
    result = ''
    while (token := tokenizer.next()).value != 'EOF':
        result += str(token) + '\n'
    return result[:-1]


def start_tests(test_path, test_count):
    for i in range(test_count):
        file_path = test_path + '{:0>3}.java'.format(i + 1)
        out = get_token_str(file_path)
        answer = get_answer(file_path)
        # if out != '':
        # print('\n{0}\n\n{1}'.format(out, answer))
        print('test {0:3} -> {1}'.format(i + 1, colored(answer == out, 'green' if answer == out else 'red')))


if __name__ == '__main__':
    start_tests('tests/', 25)
