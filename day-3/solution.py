def get_input():
    with open('input') as f:
        return [line.strip() for line in f]


def part1(input):
    gamma_rate = ''
    epsilon_rate = ''

    for i in range(len(input[0])):
        top_down_binary = [binary[i] for binary in input]
        count_zero = top_down_binary.count('0')
        count_one = top_down_binary.count('1')

        gamma_rate += '0' if count_zero > count_one else '1'
        epsilon_rate += '1' if count_zero > count_one else '0'

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def get_matching_bit_criteria(input, index, rating_type):
    top_down_binary = [binary[index] for binary in input]
    count_zero = top_down_binary.count('0')
    count_one = top_down_binary.count('1')

    if rating_type == 'oxygen':
        current_bit_criteria = '1' if count_one > count_zero else '0'
        current_bit_criteria = '1' if count_one == count_zero else current_bit_criteria
    else:
        current_bit_criteria = '1' if count_one < count_zero else '0'
        current_bit_criteria = '0' if count_one == count_zero else current_bit_criteria

    return [binary for binary in input if binary[index] == current_bit_criteria]


def part2(input):
    oxygen_generator_binaries = list(input)
    co2_generator_binaries = list(input)
    index = 0

    while len(oxygen_generator_binaries) > 1:
        oxygen_generator_binaries = get_matching_bit_criteria(oxygen_generator_binaries, index, 'oxygen')
        index += 1

    index = 0

    while len(co2_generator_binaries) > 1:
        co2_generator_binaries = get_matching_bit_criteria(co2_generator_binaries, index, 'co2')
        index += 1

    return int(oxygen_generator_binaries[0], 2) * int(co2_generator_binaries[0], 2)


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
