import time
from itertools import permutations


def get_input():
    input = []
    with open('input') as file:
        lines = [line.strip().split(' | ') for line in file]

        for line in lines:
            patterns = line[0].split()
            patterns_sorted = [''.join(sorted(pattern)) for pattern in patterns]

            output = line[1].split()
            output_sorted = [''.join(sorted(out)) for out in output]

            input.append((set(patterns_sorted), output_sorted))

    return input


def part1(input):
    return sum(len(pattern) in [2, 4, 3, 7] for entry in input for pattern in entry[1])


def part2(input):
    digit_locations = {
        0: [0, 1, 2, 4, 5, 6],
        1: [2, 5],
        2: [0, 2, 3, 4, 6],
        3: [0, 2, 3, 5, 6],
        4: [1, 2, 3, 5],
        5: [0, 1, 3, 5, 6],
        6: [0, 1, 3, 4, 5, 6],
        7: [0, 2, 5],
        8: [0, 1, 2, 3, 4, 5, 6],
        9: [0, 1, 2, 3, 5, 6]
    }

    perm = [''.join(p) for p in permutations('abcdefg')]
    total = 0
    for patterns, output in input:
        res = {}
        for p in perm:
            matching = 0
            for digit in range(0, 10):
                locations = digit_locations[digit]
                segments_for_digit = ''.join(sorted(p[i] for i in locations))
                is_matching = segments_for_digit in patterns
                if not is_matching:
                    break
                matching += 1

            if matching != 10:
                continue

            for digit in range(0, 10):
                locations = digit_locations[digit]
                segments_for_digit = ''.join(sorted(p[i] for i in locations))
                res[segments_for_digit] = digit

            value_str = ''
            for o in output:
                value_str += str(res[o])

            total += int(value_str)

    return total


input = get_input()
print('Part 1:', part1(input))
# Takes 1 sec
print('Part 2:', part2(input))
