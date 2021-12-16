from functools import reduce


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]
    return lines[0]


class Packet:

    def __init__(self, init_packet):
        self.init_packet = init_packet
        self.version = int(init_packet[0:3], 2)
        self.id = int(init_packet[3:6], 2)

        if self.id == 4:
            self.packet, self.literal_value = self.get_packet_for_literal_val()
            self.sub_packets = []
        else:
            self.operator = int(init_packet[6], 2)
            self.packet, self.sub_packets = self.get_sub_packets_by_size() if self.operator else self.get_sub_packets_by_bits()

    def get_packet_for_literal_val(self):
        init_packet = self.init_packet
        start = init_packet[:6]
        end = ''
        index = 6
        literal_value_bits = ''

        while init_packet[index] != '0':
            literal_value_bits += init_packet[index + 1:index + 5]
            end += init_packet[index:index + 5]
            index += 5

        end += init_packet[index:index + 5]
        literal_value_bits += init_packet[index + 1:index + 5]

        return start + end, int(literal_value_bits, 2)

    def get_sub_packets_by_size(self):
        init_packet = self.init_packet
        number_of_sub_packets_binary = init_packet[7:18]
        number_of_sub_packets = int(number_of_sub_packets_binary, 2)
        rem_sub_packets_extract = init_packet[18:]

        sub_packets = []
        sub_packets_extract = ''
        start = init_packet[:7]

        for _ in range(number_of_sub_packets):
            new_packet = Packet(rem_sub_packets_extract)
            sub_packets_extract += new_packet.packet
            sub_packets.append(new_packet)
            rem_sub_packets_extract = rem_sub_packets_extract[len(new_packet.packet):]

        full_packet = start + number_of_sub_packets_binary + sub_packets_extract

        return full_packet, sub_packets

    def get_sub_packets_by_bits(self):
        init_packet = self.init_packet
        number_of_bits_binary = init_packet[7:22]
        number_of_bits = int(number_of_bits_binary, 2)
        rem_sub_packets_extract = init_packet[22:22 + number_of_bits]

        sub_packets = []
        start = init_packet[:7]
        sub_packets_extract = ''

        while len(sub_packets_extract) < number_of_bits:
            new_packet = Packet(rem_sub_packets_extract)
            sub_packets_extract += new_packet.packet
            sub_packets.append(new_packet)
            rem_sub_packets_extract = rem_sub_packets_extract[len(new_packet.packet):]

        if len(sub_packets_extract) != number_of_bits:
            raise RuntimeError(f'Size of the extract should be equal to {number_of_bits}')

        full_packet = start + number_of_bits_binary + sub_packets_extract

        return full_packet, sub_packets

    def get_version_sum(self):
        return self.version + sum(sub_packet.get_version_sum() for sub_packet in self.sub_packets)

    def get_value(self):

        if self.id == 4:
            return self.literal_value

        values = [sub_packet.get_value() for sub_packet in self.sub_packets]
        if self.id == 0:
            return sum(values)

        if self.id == 1:
            return reduce(lambda x, y: x * y, values, 1)

        if self.id == 2:
            return min(values)

        if self.id == 3:
            return max(values)

        if self.id == 5:
            return int(values[0] > values[1])

        if self.id == 6:
            return int(values[0] < values[1])

        if self.id == 7:
            return int(values[0] == values[1])


def part1(root_packet):
    version = root_packet.get_version_sum()
    return version


def part2(root_packet):
    return root_packet.get_value()


def create_root_packet(init_packet):
    packet_bits = ''
    for i in init_packet:
        packet_bits += bin(int(i, 16))[2:].zfill(4)
    p = Packet(packet_bits)
    return p


input = get_input()
root_packet = create_root_packet(input)
print('Part 1:', part1(root_packet))
print('Part 2:', part2(root_packet))
