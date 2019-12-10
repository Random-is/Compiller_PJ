from contextlib import redirect_stdout
from io import StringIO
from termcolor import colored

from main.main import Main


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


def start_tests(test_path, test_count):
    for i in range(test_count):
        file_path = test_path + '{:0>3}.java'.format(i + 1)
        main = Main(file_path)
        with StringIO() as buf, redirect_stdout(buf):
            main.compile()
            out = buf.getvalue()[:-1]
        answer = get_answer(file_path)
        # if out != '':
        # print('\n{0}\n\n{1}'.format(out, answer))
        print('test {0:3} -> {1}'.format(i + 1, colored(answer == out, 'green' if answer == out else 'red')))


# start_time = time.time()
if __name__ == '__main__':
    start_tests('../assets/tests/', 25)

# for i in range(1, 100):
#     open('../assets/tests/{:0>3}.java'.format(i + 1), 'w')
# print("--- %s seconds ---" % (time.time() - start_time))