def get_input():
    points = []
    folds = []
    with open('input') as file:
        lines = [line.strip() for line in file]
        is_fold = False
        for line in lines:
            if not line:
                is_fold = True
                continue

            if not is_fold:
                split = line.split(',')
                points.append((int(split[1]), int(split[0])))
            else:
                split = line.split()
                fold = split[2].split('=')
                folds.append((fold[0], int(fold[1])))

    return points, folds


def fold_it(points, folds):

    final_points = set(points)

    for coord, val in folds:
        if coord == 'y':
            for y, x in set(final_points):
                if y > val:
                    next_y = val - (y - val)
                    final_points.remove((y, x))
                    final_points.add((next_y, x))

        if coord == 'x':
            for y, x in set(final_points):
                if x > val:
                    next_x = val - (x - val)
                    final_points.remove((y, x))
                    final_points.add((y, next_x))

    return final_points


def part1(input):
    points, folds = input
    final_points = fold_it(points, [folds[0]])
    return len(final_points)


def part2(input):
    points, folds = input
    final_points = fold_it(points, folds)
    limit_y, _ = max(final_points, key=lambda p: p[0])
    _, limit_x = max(final_points, key=lambda p: p[1])
    res = ''
    for y in range(limit_y + 1):
        for x in range(limit_x + 1):
            if (y, x) in final_points:
                res += '#'
            else:
                res += '.'
        res += '\n'

    return res


input = get_input()
print('Part 1:', part1(input))
print('Part 2:')
print(part2(input))
