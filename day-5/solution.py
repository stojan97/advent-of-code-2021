def get_input():
    segments = []
    with open('input') as file:
        lines = [line.strip().split(' -> ') for line in file]

        for line in lines:
            start = line[0].split(',')
            end = line[1].split(',')

            segment = (int(start[1]), int(start[0]), int(end[1]), int(end[0]))
            segments.append(segment)

    return segments


def solve(input, consider_diagonal):
    maxi = max(max(input, key=lambda s: max(s)))
    grid = [[0] * (maxi + 1) for i in range(maxi + 1)]

    total_above_two = 0

    for segment in input:
        y1, x1, y2, x2 = segment

        if not consider_diagonal and y1 != y2 and x1 != x2:
            continue

        while True:
            if grid[y1][x1] != -1:
                grid[y1][x1] += 1
                if grid[y1][x1] >= 2:
                    grid[y1][x1] = -1
                    total_above_two += 1

            if y1 == y2 and x1 == x2:
                break

            if y1 != y2:
                y1 += 1 if y1 < y2 else -1

            if x1 != x2:
                x1 += 1 if x1 < x2 else -1

    return total_above_two


input = get_input()
print('Part 1:', solve(input, False))
print('Part 2:', solve(input, True))
