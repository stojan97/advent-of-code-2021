def get_input():
    height_map = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            row = []
            for c in line:
                row.append(int(c))
            height_map.append(row)

    return height_map


ADJACENT = lambda i, j: [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def get_low_points(input):
    low_points = []
    for i in range(len(input)):
        for j in range(len(input[i])):
            is_low_point = True

            for x, y in ADJACENT(i, j):
                if not (x in range(0, len(input)) and y in range(0, len(input[i]))):
                    continue
                if input[i][j] >= input[x][y]:
                    is_low_point = False
                    break

            if is_low_point:
                low_points.append((i, j))

    return low_points


def part1(input):
    return sum(input[i][j] + 1 for i, j in get_low_points(input))


def dfs(i, j, visited, input):
    visited.add((i, j))
    size = 1
    for x, y in ADJACENT(i, j):
        if not (x in range(0, len(input)) and y in range(0, len(input[i]))) or (x, y) in visited or input[x][y] == 9:
            continue

        size += dfs(x, y, visited, input)

    return size


def part2(input):
    basins_sizes = [dfs(i, j, set(), input) for i, j in get_low_points(input)]
    basins_sizes.sort(reverse=True)
    return basins_sizes[0] * basins_sizes[1] * basins_sizes[2]


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
