def get_input():
    first_row = True
    boards = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        board = []
        for line in lines:
            if not line:
                if board:
                    boards.append(board)
                board = []
                continue

            if first_row:
                gen_numbers = [int(i) for i in line.split(',')]
                first_row = False
            else:
                board.append([int(i) for i in line.split()])

    boards.append(board)
    return gen_numbers, boards


def mark_board(board, gen):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = -1 if board[i][j] == gen else board[i][j]


def check_win(board):
    for row in board:
        count = row.count(-1)
        if count == len(row):
            return True

    for j in range(len(board[0])):
        top_down = [board[i][j] for i in range(len(board))]
        count = top_down.count(-1)
        if count == len(top_down):
            return True

    return False


def sum_unmarked(board):
    return sum(cell for row in board for cell in row if cell != -1)


def solve_parts(input):
    gen_numbers, boards = input
    first_time = True
    first_score, last_score = -1, -1
    for gen in gen_numbers:
        for index in range(len(boards)):
            board = boards[index]
            if not board:
                continue

            mark_board(board, gen)
            if check_win(board):
                score = gen * sum_unmarked(board)
                if first_time:
                    first_score = score
                    first_time = False

                boards[index] = []
                last_score = score

    return first_score, last_score


input = get_input()
part1, part2 = solve_parts(input)
print('Part 1: ', part1)
print('Part 2: ', part2)
