import pandas


def generate_table(excel_path):
    excel = pandas.read_excel(excel_path)
    state_table = []
    for i in range(19):
        row = []
        for j in range(1, 98):
            row.append(excel.iat[i, j])
        state_table.append(tuple(row))
    state_table = str(tuple(state_table)).replace("'", '')
    file_text = "table_str = '" + state_table + "'"
    file = open('../table.py', 'w')
    file.write(file_text)
    file.close()


if __name__ == '__main__':
    generate_table('sm.xlsx')
