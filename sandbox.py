TEST_BOARD = [['O', 'C', 'L', 'E', 'Q'],
              ['D', 'N', 'P', 'B', 'D'],
              ['Z', 'L', 'C', 'W', 'J'],
              ['H', 'D', 'S', 'O', 'V'],
              ['T', 'N', 'Y', 'S', 'V']]


def read_dict(dict_path):
    """Read and return all words in dictionary."""

    dict_file = open(dict_path)
    words = [w.strip() for w in dict_file]
    dict_file.close()
    return words


def look_around(row, cell):
    print('looking at position', row, cell)


words_list = read_dict("words.txt")

for row in range(len(TEST_BOARD)):
    row_data = TEST_BOARD[row]
    for cell in range(len(row_data)):
        look_around(row, cell)
