import math
import time
from copy import deepcopy
from heapq import heapify, heappop, heappush


def get_input():
    grid = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            grid.append([int(i) for i in line])

    return grid


adj = lambda i, j: [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def get_shortest_risk(grid):
    row = len(grid)
    col = len(grid[0])
    pq = [(0, 0, 0)]
    heapify(pq)
    visited = set()
    d = [[math.inf] * col for _ in range(row)]
    d[0][0] = 0

    while pq:
        dist_so_far, i, j = heappop(pq)

        if i == row - 1 and j == col - 1:
            return dist_so_far

        if (i, j) in visited:
            continue

        visited.add((i, j))

        for x, y in adj(i, j):
            if 0 <= x < row and 0 <= y < col:
                next_dist = dist_so_far + grid[x][y]
                if next_dist < d[x][y]:
                    d[x][y] = next_dist
                    heappush(pq, (next_dist, x, y))

    return -1


def part1(grid):
    return get_shortest_risk(grid)


def increase_row(row):
    return [1 if value == 9 else value + 1 for value in row]


def part2(grid):
    big_grid = deepcopy(grid)

    limit = 4
    row = len(grid)
    col = len(grid[0])
    for i in range(row):
        for c in range(limit):
            col_ = big_grid[i][-col:]
            big_grid[i] += increase_row(col_)

    for z in range(limit):

        for i in range(row):
            big_grid.append(increase_row(big_grid[-row][:row]))

        for i in range(row, 0, -1):
            current_row = -i
            for c in range(limit):
                col_ = big_grid[current_row][-col:]
                big_grid[current_row] += increase_row(col_)

    return get_shortest_risk(big_grid)


input = get_input()
print('Part 1:', part1(input))
# runs around 0.9 - 1 sec
print('Part 2:', part2(input))