import re
import time


def get_input():
    instructions = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            state = line.split()[0]
            cuboid = tuple(map(int, re.sub(r'[^-\d]', ' ', line).strip().split()))
            instructions.append((state == 'on', cuboid))

    return instructions


def get_cubes(index, coordinate):
    return coordinate[index + 1] - coordinate[index]


def part2(instructions):
    xs = set()
    ys = set()
    zs = set()

    for _, (x1, x2, y1, y2, z1, z2) in instructions:
        xs.update({x1, x2 + 1})
        ys.update({y1, y2 + 1})
        zs.update({z1, z2 + 1})

    xl = sorted(list(xs))
    yl = sorted(list(ys))
    zl = sorted(list(zs))

    # compressed turned_on
    turned_on = set()

    for idx, instruction in enumerate(instructions):
        state, (x1, x2, y1, y2, z1, z2) = instruction
        x1_idx, x2_idx = xl.index(x1), xl.index(x2 + 1)
        y1_idx, y2_idx = yl.index(y1), yl.index(y2 + 1)
        z1_idx, z2_idx = zl.index(z1), zl.index(z2 + 1)

        for x in range(x1_idx, x2_idx):
            for y in range(y1_idx, y2_idx):
                for z in range(z1_idx, z2_idx):
                    if state:
                        turned_on.add((x, y, z))
                    else:
                        turned_on.discard((x, y, z))

    return sum(get_cubes(x, xl) * get_cubes(y, yl) * get_cubes(z, zl) for x, y, z in turned_on)


start = time.time()
input = get_input()
print('Part 2:', part2(input))
print(time.time() - start)
