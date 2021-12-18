import math
import re
from math import floor, ceil


def get_input():
    parsed = []
    with open('input') as file:
        lines = [line.strip() for line in file]

    for line in lines:
        extract_numbers = re.sub(r'[^\d]', ' ', line).split()
        num_reached = False
        parsed_line = []
        index = 0
        for c in line:
            if c.isnumeric() and not num_reached:
                parsed_line.append(extract_numbers[index])
                index += 1
                num_reached = True

            if not c.isnumeric():
                num_reached = False
                parsed_line.append(c)

        parsed.append(parsed_line)

    return parsed


def to_str(pair):
    return ''.join(pair)


def explode(pairs):
    i = 0
    opened = 0
    last_number_index = -1
    explosion = 1
    while i < len(pairs) - 2:
        opened += pairs[i] == '['
        opened -= pairs[i] == ']'

        if pairs[i].isnumeric() and pairs[i + 2].isnumeric() and opened == 5:
            # do explode
            first = pairs[i]
            second = pairs[i + 2]

            if last_number_index != -1:
                pairs[last_number_index] = str(int(pairs[last_number_index]) + int(first))

            for j in range(i + 3, len(pairs)):
                if pairs[j].isnumeric():
                    pairs[j] = str(int(pairs[j]) + int(second))
                    break

            pairs = pairs[:i - 1] + ['0'] + pairs[i + 4:]
            explosion += 1
            i = 0
            last_number_index = -1
            opened = 0
            continue

        if pairs[i].isnumeric():
            last_number_index = i

        i += 1

    return pairs


def split(pairs):
    i = 0
    opened = 0
    last_number_index = -1
    splits = 1
    while i < len(pairs):
        opened += pairs[i] == '['
        opened -= pairs[i] == ']'

        if pairs[i].isnumeric() and int(pairs[i]) >= 10:
            left = str(floor(int(pairs[i]) / 2))
            right = str(ceil(int(pairs[i]) / 2))

            if opened == 4:
                if last_number_index != -1:
                    pairs[last_number_index] = str(int(pairs[last_number_index]) + int(left))

                for j in range(i + 1, len(pairs)):
                    if pairs[j].isnumeric():
                        pairs[j] = str(int(pairs[j]) + int(right))
                        break

                pairs[i] = '0'
            else:
                split = ['[', left, ',', right, ']']
                pairs = pairs[:i] + split + pairs[i + 1:]

            splits += 1
            i = 0
            last_number_index = -1
            opened = 0
            continue

        if pairs[i].isnumeric():
            last_number_index = i

        i += 1

    return pairs


def reduce(pair):
    pair = explode(pair)
    pair = split(pair)
    return pair


def add(pair1, pair2):
    res = ['[']
    res += pair1
    res.append(',')
    res += pair2
    res.append(']')
    return res


def get_magnitude(pair):
    i = 0

    while i < len(pair) - 2:
        left = pair[i]
        right = pair[i + 2]
        if left.isnumeric() and right.isnumeric():
            m = str(3 * int(left) + 2 * int(right))
            pair = pair[:i - 1] + [m] + pair[i + 4:]
            i = 0
            continue

        i += 1

    return int(pair[0])


def part1(pairs):
    res = pairs[0]

    for i in range(1, len(pairs)):
        res = add(res, pairs[i])
        res = reduce(res)

    return get_magnitude(res)


def part2(pairs):
    max_magnitude = -math.inf
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            if i != j:
                res = add(pairs[i], pairs[j])
                res = reduce(res)
                max_magnitude = max(max_magnitude, get_magnitude(res))

    return max_magnitude


input = get_input()
print('Part 1:', part1(input))
# 1 sec
print('Part 2:', part2(input))
