def get_input():
    with open('input') as f:
        input = [int(line.strip()) for line in f]

    return input


def part1(input):
    return sum(current > prev for prev, current in zip(input, input[1:]))


def part2(input):
    res = [a + b + c for a, b, c in zip(input, input[1:], input[2:])]
    return part1(res)


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
