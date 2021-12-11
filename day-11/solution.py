def get_input():
    grid = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            grid.append([int(i) for i in line])

    return grid


ADJACENT = lambda i, j: [
    (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
    (i, j - 1), (i, j + 1),
    (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]


def dfs(i, j, grid, visited):
    visited.add((i, j))
    produced_flashes = []
    for x, y in ADJACENT(i, j):
        if x in range(len(grid)) and y in range(len(grid[i])):
            grid[x][y] += 1

            if grid[x][y] > 9:
                produced_flashes.append((x, y))

    for x, y in produced_flashes:
        if (x, y) not in visited:
            dfs(x, y, grid, visited)


def get_flashes(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] += 1

    visited = set()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] > 9 and (i, j) not in visited:
                dfs(i, j, grid, visited)

    flashes = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] > 9:
                grid[i][j] = 0
                flashes += 1

    return flashes


def part1(input):
    grid = [list(i) for i in input]
    return sum(get_flashes(grid) for _ in range(100))


def part2(grid):
    step = 1

    while True:
        flashes = get_flashes(grid)
        if flashes == len(grid) * len(grid[0]):
            break
        step += 1

    return step


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
