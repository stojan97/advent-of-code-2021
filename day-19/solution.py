import time
from collections import deque


def get_input():
    scanners = []
    beans = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            if not line:
                continue

            if 'scanner' in line:
                if beans:
                    scanners.append(beans)

                beans = []
                continue

            split = line.split(',')
            bean = tuple(map(int, split))
            beans.append(bean)

        scanners.append(beans)

    return scanners


def find_intersecting_orientation_for_next_scanner(current_orientation, orientations):
    relocations_for_all_points = []

    for current_point in current_orientation:
        x1, y1, z1 = current_point
        relocations = [(x - x1, y - y1, z - z1) for x, y, z in current_orientation]
        relocations_for_all_points.append((current_point, relocations))

    for orientation in orientations:
        orientation_set = set(orientation)
        for point in orientation:
            x1, y1, z1 = point

            for relocating_point, point_relocations_to_other_points in relocations_for_all_points:
                intersecting_points = 0
                for relocation in point_relocations_to_other_points:
                    x, y, z = relocation
                    final_point = (x1 + x, y1 + y, z1 + z)
                    if final_point in orientation_set:
                        intersecting_points += 1

                if intersecting_points >= 12:
                    next_scanner_point_relocations_to_other_points = [(x - x1, y - y1, z - z1) for x, y, z in orientation]
                    x_p, y_p, z_p = relocating_point
                    scanner_point_relative_to_start = (x_p - x1, y_p - y1, z_p - z1)
                    next_orientation = [(x_p + x, y_p + y, z_p + z) for x, y, z in next_scanner_point_relocations_to_other_points]
                    return next_orientation, scanner_point_relative_to_start

    return None, None


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def solve(scanners):
    stack = deque()
    _, init_orientation_points = scanners[0]
    stack.append((0, init_orientation_points))
    visited = set()
    visited.add(0)
    explored_points = set()
    all_scanners = [(0, 0, 0)]

    while stack:
        i, current_orientation = stack.pop()
        explored_points.update(current_orientation)
        print('Processing scanner:', i)
        for j in range(len(scanners)):
            if j in visited:
                continue

            orientations, _ = scanners[j]
            next_orientation, next_scanner = find_intersecting_orientation_for_next_scanner(current_orientation, orientations)

            if next_orientation:
                stack.append((j, next_orientation))
                visited.add(j)
                all_scanners.append(next_scanner)

    max_dist = 0
    for i in range(len(all_scanners)):
        for j in range(i + 1, len(all_scanners)):
            max_dist = max(max_dist, dist(all_scanners[i], all_scanners[j]))

    return len(explored_points), max_dist


def get_orientations(x, y, z, rotate_by):
    # z is rotating axis
    rots = {'x': [(z, x, y), (z, -x, -y), (z, y, -x), (z, -y, x)],
            '-x': [(-z, y, x), (-z, -y, -x), (-z, x, -y), (-z, -x, y)],
            'y': [(y, z, x), (x, z, -y), (-y, z, -x), (-x, z, y)],
            '-y': [(x, -z, y), (-x, -z, -y), (y, -z, -x), (-y, -z, x)],
            'z': [(x, y, z), (-x, -y, z), (y, -x, z), (-y, x, z)],
            '-z': [(y, x, -z), (-y, -x, -z), (x, -y, -z), (-x, y, -z)]}

    return rots[rotate_by]


def get_all_orientations_for_scanner(init_orientation):
    orientations = []
    rotate_by_axis = ['x', '-x', 'y', '-y', 'z', '-z']

    for rotate_by in rotate_by_axis:
        rot1 = list(get_orientations(x, y, z, rotate_by)[0] for x, y, z in init_orientation)
        rot2 = list(get_orientations(x, y, z, rotate_by)[1] for x, y, z in init_orientation)
        rot3 = list(get_orientations(x, y, z, rotate_by)[2] for x, y, z in init_orientation)
        rot4 = list(get_orientations(x, y, z, rotate_by)[3] for x, y, z in init_orientation)
        orientations.append(rot1)
        orientations.append(rot2)
        orientations.append(rot3)
        orientations.append(rot4)

    return orientations


def parse_scanners(input):
    scanners = []
    for i in range(len(input)):
        init_orientation = input[i]
        orientations = get_all_orientations_for_scanner(init_orientation)
        scanner = (orientations, init_orientation)
        scanners.append(scanner)

    return scanners


input = get_input()
scanners = parse_scanners(input)
start = time.time()
# 27 seconds on average.
part1, part2 = solve(scanners)
print(time.time() - start)
print('Part 1:', part1)
print('Part 2:', part2)
