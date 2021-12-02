def get_input():
    with open('input') as f:
        return [tuple(line.strip().split()) for line in f]


move_func = [{
    'forward': (lambda x, y, aim, u: (x + u, y, aim)),
    'down': (lambda x, y, aim, u: (x, y + u, aim)),
    'up': (lambda x, y, aim, u: (x, y - u, aim))
}, {

    'forward': (lambda x, y, aim, u: (x + u, y + (aim * u), aim)),
    'down': (lambda x, y, aim, u: (x, y, aim + u)),
    'up': (lambda x, y, aim, u: (x, y, aim - u))
}]


def solve_part(input, part):
    x = y = aim = 0

    for dir, units in input:
        u = int(units)
        move = move_func[part][dir]
        x, y, aim = move(x, y, aim, u)

    return x * y


input = get_input()
print(solve_part(input, 0))
print(solve_part(input, 1))
