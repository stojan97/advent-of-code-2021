from collections import deque


def get_input():
    instructions = []
    with open('input') as file:
        lines = [line.strip() for line in file]

    for line in lines:
        split = tuple(line.split())
        instructions.append(split)

    groups = []
    current_group = []

    for instruction in instructions:
        if instruction[0] == 'inp':
            groups.append(current_group)
            current_group = []
            continue

        current_group.append(instruction)

    groups.append(current_group)
    groups.pop(0)

    reduced_instructions = []

    for i in range(len(groups)):
        reduced_instructions.append((int(groups[i][-3][2]), int(groups[i][4][2]), ('div', 'z', '26') in groups[i]))

    matching_pair = [0] * len(reduced_instructions)
    stack = deque()

    for idx, reduced_instruction in enumerate(reduced_instructions):
        if reduced_instruction[2]:
            pop = stack.pop()
            matching_pair[pop] = idx
            matching_pair[idx] = pop
        else:
            stack.append(idx)

    return reduced_instructions, matching_pair


def find_input(matching_pair, input, instructions, minimize):
    for i in range(len(instructions)):
        _, subtract_const, inverse_instruction = instructions[i]
        if inverse_instruction:
            # find the matching instruction
            add_const, _, _ = instructions[matching_pair[i]]
            diff = add_const + subtract_const

            if diff < 0:
                if minimize:
                    input[matching_pair[i]] += abs(diff)
                else:
                    input[i] -= abs(diff)
            else:
                if minimize:
                    input[i] += abs(diff)
                else:
                    input[matching_pair[i]] -= abs(diff)

    return ''.join(map(str, input))


def solve(instructions, matching_pair):
    # We can construct matching pairs from the procedures, (normal procedure, inverse procedure)
    maximized = find_input(matching_pair, [9] * len(instructions), instructions, False)
    minimized = find_input(matching_pair, [1] * len(instructions), instructions, True)

    return maximized, minimized


instructions, matching_pair = get_input()
part1, part2 = solve(instructions, matching_pair)
print('Part 1:', part1)
print('Part 2:', part2)