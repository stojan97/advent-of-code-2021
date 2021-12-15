import math
from collections import defaultdict
from copy import copy


def get_input():
    polymer = ''
    insertion_rules = {}
    with open('input') as file:
        lines = [line.strip() for line in file]
        is_polymer = True
        for line in lines:
            if not line:
                is_polymer = False
                continue

            if is_polymer:
                polymer = line
            else:
                split = line.split(' -> ')
                insertion_rules[split[0]] = split[1]

    return (polymer, insertion_rules)


def part1(input):
    polymer, insertion_rules = input
    for i in range(10):
        next_polymer = polymer[0]
        for j in range(1, len(polymer)):
            pair = polymer[j - 1] + polymer[j]
            if pair in insertion_rules:
                next_polymer += insertion_rules[pair] + polymer[j]
            else:
                next_polymer += polymer[j]

        polymer = next_polymer

    c = defaultdict(int)

    for i in polymer:
        c[i] += 1

    max_res = c[max(c, key=c.get)]
    min_res = c[min(c, key=c.get)]

    return max_res - min_res


def part2(input):
    polymer, insertion_rules = input
    pairs = defaultdict(int)

    for j in range(1, len(polymer)):
        pair = polymer[j - 1] + polymer[j]
        pairs[pair] += 1

    for i in range(40):
        copy_pairs = copy(pairs)
        for k, v in pairs.items():
            if k in insertion_rules:
                copy_pairs[k] -= v
                copy_pairs[k[0] + insertion_rules[k]] += v
                copy_pairs[insertion_rules[k] + k[1]] += v

        pairs = copy_pairs

    c = defaultdict(int)

    for k, v in pairs.items():
        c[k[0]] += v
        c[k[1]] += v

    for k in copy(c):
        c[k] = math.ceil(c[k] / 2)

    c[polymer[0]] += polymer[0] == polymer[-1]

    max_res = c[max(c, key=c.get)]
    min_res = c[min(c, key=c.get)]

    return max_res - min_res


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
