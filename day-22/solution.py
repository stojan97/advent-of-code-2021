import re
import time
from copy import copy


def get_input():
    cuboids = []
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            state = line.split()[0]
            cuboid = tuple(map(int, re.sub(r'[^-\d]', ' ', line).strip().split()))
            cuboids.append((state == 'on', cuboid))

    return cuboids


def part1(cuboids):
    present_points = set()

    for state, (x1, x2, y1, y2, z1, z2) in cuboids:
        if x2 < -50 or x1 > 50 or y2 < -50 or y1 > 50 or z2 < -50 or z1 > 50:
            continue

        for x in range(max(x1, -50), min(x2 + 1, 51)):
            for y in range(max(y1, -50), min(y2 + 1, 51)):
                for z in range(max(z1, -50), min(z2 + 1, 51)):
                    if state:
                        present_points.add((x, y, z))
                    else:
                        present_points.discard((x, y, z))

    return len(present_points)


def check(first, second):
    start1, end1 = first
    start2, end2 = second

    return min(end1, end2) >= max(start1, start2)


def get_intersection(source, target):
    x11, x21, y11, y21, z11, z21 = source
    x12, x22, y12, y22, z12, z22 = target
    if check((x11, x21), (x12, x22)) and check((y11, y21), (y12, y22)) and check((z11, z21), (z12, z22)):
        x1 = max(x11, x12)
        x2 = min(x21, x22)
        y1 = max(y11, y12)
        y2 = min(y21, y22)
        z1 = max(z11, z12)
        z2 = min(z21, z22)
        return x1, x2, y1, y2, z1, z2

    return None


def get_slices(target, intersection):
    ix1, ix2, iy1, iy2, iz1, iz2 = intersection
    x1, x2, y1, y2, z1, z2 = target
    slices = set()

    # slice from side (by z)

    if z2 > iz2:
        # TOP
        side_top_slice = (x1, x2, y1, y2, iz2 + 1, z2)
        slices.add(side_top_slice)

    if z1 < iz1:
        # BOTTOM
        side_bot_slice = (x1, x2, y1, y2, z1, iz1 - 1)
        slices.add(side_bot_slice)

    if y1 < iy1:
        # LEFT
        side_left_slice = (x1, x2, y1, iy1 - 1, iz1, iz2)
        slices.add(side_left_slice)

    if y2 > iy2:
        # RIGHT
        side_right_slice = (x1, x2, iy2 + 1, y2, iz1, iz2)
        slices.add(side_right_slice)

    if x1 < ix1:
        # BACK
        side_back_slice = (x1, ix1 - 1, iy1, iy2, iz1, iz2)
        slices.add(side_back_slice)

    if x2 > ix2:
        # FRONT
        side_front_slice = (ix2 + 1, x2, iy1, iy2, iz1, iz2)
        slices.add(side_front_slice)

    return slices


def is_target_completely_inside(cuboid, target):
    x1c, x2c, y1c, y2c, z1c, z2c = cuboid
    x1t, x2t, y1t, y2t, z1t, z2t = target

    return x1t >= x1c and x2t <= x2c and y1t >= y1c and y2t <= y2c and z1t >= z1c and z2t <= z2c


def get_cubes(cuboid):
    x1, x2, y1, y2, z1, z2 = cuboid
    diff_x = (x2 - x1) + 1
    diff_y = (y2 - y1) + 1
    diff_z = (z2 - z1) + 1
    total_cubes = diff_x * diff_y * diff_z

    return total_cubes


def part2(cuboids):
    present_cuboids = set()

    for state, cuboid in cuboids:
        for other_cuboid in copy(present_cuboids):
            intersection = get_intersection(cuboid, other_cuboid)
            if intersection:
                # first remove other intersecting cuboid
                present_cuboids.discard(other_cuboid)
                slices_from_other = get_slices(other_cuboid, intersection)
                # push slices from other intersecting cuboid
                present_cuboids.update(slices_from_other)

        if state:
            present_cuboids.add(cuboid)

    res = sum(get_cubes(cuboid) for cuboid in present_cuboids)

    return res


input = get_input()
print('Part 1:', part1(input))
start = time.time()
print('Part 2:', part2(input))
print((time.time() - start))
