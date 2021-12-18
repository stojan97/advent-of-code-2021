import math
import re


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    first_line = lines[0]

    split = first_line.split()
    split[2] = re.sub(r'[^-\d]', ' ', split[2])
    split[3] = re.sub(r'[^-\d]', ' ', split[3])

    split_x = split[2].split()
    split_y = split[3].split()

    return (int(split_x[0]), int(split_x[1])), (int(split_y[0]), int(split_y[1]))


def hit_x(x, x1, x2):
    return x1 <= x <= x2


def hit_y(y, y1, y2):
    return y1 >= y >= y2


def hit_target(x, y, input):
    (x1, x2), (y2, y1) = input
    return hit_x(x, x1, x2) and hit_y(y, y1, y2)


def simulate(x_velocity, y_velocity, input):
    (x1, x2), (y1, y2) = input
    x, y = 0, 0
    highest_y = 0

    while x <= x2 and y >= y1:
        if hit_target(x, y, input):
            return True, highest_y, x, y, x_velocity, y_velocity

        highest_y = max(highest_y, y)

        x += x_velocity
        y += y_velocity
        x_velocity -= 1 if x_velocity > 0 else 0
        y_velocity -= 1

    return False, highest_y, x, y, x_velocity, y_velocity


def summation(n):
    return (n * (n + 1)) // 2


def part1_formula(input):
    _, (y1, y2) = input
    return summation(abs(y1 + 1))

def solve(input):
    (x1, x2), (y1, y2) = input
    max_y = -math.inf
    count = 0

    for x_velocity in range(1, x2 + 1):
        peak_x = summation(x_velocity)
        if peak_x < x1:
            continue

        for y_velocity in range(y1, abs(y1) + 1):

            reached_target, highest_y, x, y, x_res_vel, y_res_vel = simulate(x_velocity, y_velocity, input)

            if reached_target:
                max_y = max(max_y, highest_y)
                count += 1

            y_velocity += 1

    return max_y, count


input = get_input()
part1, part2 = solve(input)
print(f'Part 1: {part1}, formula={part1_formula(input)}')
print('Part 2:', part2)
