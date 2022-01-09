import time


def get_input():
    image = []
    with open('input') as file:
        lines = [line.strip() for line in file]
        first = True
        for line in lines:
            if first:
                algorithm = line
                first = False
                continue

            if not line:
                continue

            image.append(line)

    return algorithm, image


def adj(i, j):
    return [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
            (i, j - 1), (i, j), (i, j + 1),
            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
            ]


def solve(input, n):
    algorithm, image = input

    # convert to 1s and 0s
    input = [['0'] * len(image[i]) for i in range(len(image))]

    for i in range(len(image)):
        for j in range(len(image[i])):
            input[i][j] = '1' if image[i][j] == '#' else '0'

    pixels = {}

    for i in range(len(image)):
        for j in range(len(image[i])):
            pixels[(i, j)] = input[i][j]

    next_alone_pixel = '0'

    for k in range(n):
        new_pixels = {}
        mini = min(pixels)[0] - 1
        maxi = max(pixels)[0] + 1

        for i in range(mini, maxi + 1):
            for j in range(mini, maxi + 1):
                str = ''.join(pixels.get((x, y), next_alone_pixel) for x, y in adj(i, j))
                dec = int(str, 2)
                pixel = algorithm[dec]
                new_pixels[(i, j)] = '1' if pixel == '#' else '0'

        if algorithm[0] == '#':
            index = 0 if k % 2 == 0 else 511
            next_alone_pixel = '1' if algorithm[index] == '#' else '0'

        pixels = new_pixels

    return sum(v == '1' for v in pixels.values())


input = get_input()
start = time.time()
# executes around 2 secs for puzzle input
print('Part 1:', solve(input, 2))
print('Part 2:', solve(input, 50))
print(time.time() - start)
