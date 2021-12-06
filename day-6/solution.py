from collections import defaultdict


def get_input():
    with open('input') as file:
        lines = [line.strip().split(',') for line in file][0]

    lines = list(map(int, lines))
    return lines


def part1(input):
    for t in range(1, 81):

        for i in range(len(input)):
            if input[i] == 0:
                input[i] = 6
                input.append(8)
            else:
                input[i] -= 1

    return len(input)


def part2(input):
    dict = defaultdict(int)

    for fish in input:
        dict[fish] += 1

    for t in range(1, 257):
        items = list(dict.items())
        for fish, val in items:
            if fish == 0:
                dict[0] -= val
                dict[6] += val
                dict[8] += val
            else:
                dict[fish - 1] += val
                dict[fish] -= val

    total = 0
    for key, val in dict.items():
        total += val

    return total


input = get_input()
print('Part 1:', part1(list(input)))
print('Part 2:', part2(list(input)))
