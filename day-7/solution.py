import math


def get_input():
    with open('input') as file:
        lines = [line.strip().split(',') for line in file][0]

    lines = list(map(int, lines))
    return lines


def part1(positions):
    min_fuel = math.inf
    limit = range(min(positions), max(positions) + 1)

    for pos in limit:
        fuel = sum(abs(pos - other_pos) for other_pos in positions)
        min_fuel = min(min_fuel, fuel)

    return min_fuel


def s(n):
    return (n * (n + 1)) // 2


def part2(positions):
    min_fuel = math.inf
    limit = range(min(positions), max(positions) + 1)

    for pos in limit:
        fuel = sum(s(abs(pos - other_pos)) for other_pos in positions)
        min_fuel = min(min_fuel, fuel)

    return min_fuel


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))