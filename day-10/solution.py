from collections import deque
from statistics import median


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]
    return lines


CLOSING_FOR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

OPENING = set(CLOSING_FOR.keys())


def get_first_corrupted(line):
    stack = deque()

    for current in line:
        if current in OPENING:
            stack.append(current)
        else:
            rightmost_opening = stack.pop()
            if current != CLOSING_FOR[rightmost_opening]:
                return current

    return 'INCOMPLETE'


def part1(input):
    total = 0
    error_cost = {')': 3, ']': 57, '}': 1197, '>': 25137}

    for line in input:
        closing = get_first_corrupted(line)
        if closing == 'INCOMPLETE':
            continue
        total += error_cost[closing]

    return total


def get_total_points(line):
    stack = deque()

    for current in line:
        if current in OPENING:
            stack.append(current)
        else:
            stack.pop()

    total = 0
    points = {')': 1, ']': 2, '}': 3, '>': 4}

    while stack:
        total *= 5
        total += points[CLOSING_FOR[stack.pop()]]

    return total


def part2(input):
    incomplete = [line for line in input if get_first_corrupted(line) == 'INCOMPLETE']
    return median([get_total_points(line) for line in incomplete])


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
