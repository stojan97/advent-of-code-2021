from copy import deepcopy


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]
    return lines


def part1(grid):
    for i in range(len(grid)):
        grid[i] = list(grid[i])

    step = 1
    while True:
        new_grid = deepcopy(grid)
        movement = 0
        for i in range(len(grid)):
            j = 0
            while j < len(grid[0]):
                next = (j + 1) % len(grid[0])
                if grid[i][j] == '>' and grid[i][next] == '.':
                    new_grid[i][j] = '.'
                    new_grid[i][next] = '>'
                    j += 1
                    movement += 1
                j += 1

        grid = deepcopy(new_grid)

        for j in range(len(grid[0])):
            i = 0
            while i < len(grid):
                next = (i + 1) % len(grid)
                if grid[i][j] == 'v' and grid[next][j] == '.':
                    new_grid[i][j] = '.'
                    new_grid[next][j] = 'v'
                    i += 1
                    movement += 1
                i += 1

        grid = new_grid
        print('After step:', step, 'movement=', movement)

        if movement == 0:
            break
        step += 1

    return step


input = get_input()
print('Part 1:', part1(input))
print('Part 2: is unlocked by getting all stars')
