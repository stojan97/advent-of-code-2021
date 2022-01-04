import time
from collections import deque
from copy import copy
from heapq import *


class Amphipod:

    def __init__(self, idx, type, home_locations, energy) -> None:
        self.idx = idx
        self.type = type
        self.home_locations = home_locations
        self.energy = energy

    def __repr__(self) -> str:
        return f'Amphipod (idx={self.idx}, type={self.type}, home_locations={self.home_locations}, energy={self.energy})'

    def is_home(self, location_for: dict):
        return location_for[self.idx] in self.home_locations


class State:

    def __init__(self, total_energy, amphipod, amphipod_for) -> None:
        self.total_energy = total_energy
        self.amphipod = amphipod
        self.amphipod_for = amphipod_for

    def __lt__(self, other: 'State'):
        return self.total_energy < other.total_energy

    def __repr__(self) -> str:
        return f'State (current_amphipod={self.amphipod}, amphipod_for={self.amphipod_for}'

    def __eq__(self, o: 'State') -> bool:
        return self.amphipod == o.amphipod and self.amphipod_for == o.amphipod_for

    def __hash__(self) -> int:
        amphipod_for_items = tuple(sorted(self.amphipod_for.items()))
        return hash((self.amphipod, amphipod_for_items))


def add_edge(first, second, nodes):
    nodes[first].append(second)
    nodes[second].append(first)


def invert_dict(amphipod_for: dict):
    return {v: k for k, v in amphipod_for.items()}

def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    lines[3] = '##' + lines[3]

    first_row = ''.join(filter(str.isalpha, lines[3]))
    second_row = 'DBAC'
    third_row = 'DCBA'
    fourth_row = ''.join(filter(str.isalpha, lines[2]))

    nodes = [[] for _ in range(27)]
    g_index = 0
    amphipods = []
    energy = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    home = {
        'A': [0, 1, 2, 3],
        'B': [4, 5, 6, 7],
        'C': [8, 9, 10, 11],
        'D': [12, 13, 14, 15]
    }

    for index in range(len(first_row)):
        first_cell = first_row[index]
        second_cell = second_row[index]
        third_cell = third_row[index]
        fourth_cell = fourth_row[index]

        first = Amphipod(g_index, first_cell, home[first_cell], energy[first_cell])
        second = Amphipod(g_index + 1, second_cell, home[second_cell], energy[second_cell])
        third = Amphipod(g_index + 2, third_cell, home[third_cell], energy[third_cell])
        fourth = Amphipod(g_index + 3, fourth_cell, home[fourth_cell], energy[fourth_cell])

        amphipods += [first, second, third, fourth]
        add_edge(g_index, g_index + 1, nodes)
        add_edge(g_index + 1, g_index + 2, nodes)
        add_edge(g_index + 2, g_index + 3, nodes)

        g_index += 4

    next_room = 3

    for index in range(16, 27):

        if index not in [16, 26] and index % 2 == 0:
            add_edge(index, next_room, nodes)
            next_room += 4

        if index != 16:
            add_edge(index, index - 1, nodes)

    return amphipods, nodes


def all_covered(amphipods, location_for):
    return all(amphipod.is_home(location_for) for amphipod in amphipods)


def get_covered(amphipods, location_for):
    return sum(amphipod.is_home(location_for) for amphipod in amphipods)


def are_all_stacked(amphipods, start, limit, amphipod_for, add, location_for):
    if start == limit:
        return True

    return all(location in amphipod_for and amphipods[amphipod_for[location]].is_home(location_for) for location in range(start, limit + add))


SKIP_ROOMS = {18, 20, 22, 24} | {i for i in range(16)}
TOP_ROOMS = {16, 17, 19, 21, 23, 25, 26}


def get_possible_next_nodes(nodes, amphipod_idx, amphipod_for, amphipods, location_for):
    start_location = location_for[amphipod_idx]
    home_locations = amphipods[amphipod_idx].home_locations
    amphipod_energy = amphipods[amphipod_idx].energy
    home_locations_set = set(home_locations)

    stacked_same_kind = start_location in home_locations_set and are_all_stacked(amphipods, home_locations[0], start_location, amphipod_for, 1, location_for)

    if stacked_same_kind:
        return {}

    dist = {}
    q = deque([(start_location, 0)])

    visited = set(amphipod_for.keys())
    to_skip = set(SKIP_ROOMS)
    to_skip.difference_update(home_locations_set)

    while q:
        next_node, energy = q.popleft()
        energy_so_far = energy + amphipod_energy

        for node in nodes[next_node]:
            if node not in visited:
                if node not in to_skip:
                    dist[node] = energy_so_far
                visited.add(node)
                q.append((node, energy_so_far))

    first_home_node = next(filter(lambda n: n in dist, home_locations), None)

    if first_home_node is not None and are_all_stacked(amphipods, home_locations[0], first_home_node, amphipod_for, 0, location_for):
        return {first_home_node: dist[first_home_node]}

    # amphipod was locked
    if start_location in TOP_ROOMS:
        return {}

    for home_node in home_locations:
        if home_node in dist:
            dist.pop(home_node)

    return dist

def solve(input):
    amphipods, nodes = input
    pq = []
    heapify(pq)
    amphipod_for = {i: i for i in range(16)}

    for i in range(3, 16, 4):
        st = (State(0, i, copy(amphipod_for)))
        heappush(pq, st)

    c = 0

    memo = set()

    while pq:
        state = heappop(pq)
        total_energy = state.total_energy
        amphipod_idx = state.amphipod
        current_amphipod_for = state.amphipod_for
        location_for = invert_dict(current_amphipod_for)
        amphipod_location = location_for[amphipod_idx]

        if state in memo:
            continue

        memo.add(state)

        covered = get_covered(amphipods, location_for)
        if c % 10000 == 0:
            print(f'Covered: {covered}, energy={total_energy}, count={c}')

        c += 1

        if all_covered(amphipods, location_for):
            print(f'Covered: {covered}, energy={total_energy}, count={c}')
            return total_energy

        possible_next_nodes = get_possible_next_nodes(nodes, amphipod_idx, current_amphipod_for, amphipods, location_for)

        for next_location, energy in possible_next_nodes.items():
            next_energy = total_energy + energy
            next_amphipod_for = copy(current_amphipod_for)
            next_amphipod_for.pop(amphipod_location)
            next_amphipod_for[next_location] = amphipod_idx

            for next_amphipod_idx, _ in enumerate(amphipods):
                if next_amphipod_idx != amphipod_idx:
                    new_state = State(next_energy, next_amphipod_idx, next_amphipod_for)
                    heappush(pq, new_state)

    return -1


input = get_input()
amphipods, nodes = input
print(*amphipods, sep='\n')
print(*nodes, sep='\n')
# executes around 1 minute and 30 seconds for inputs with a lot of combinations
start = time.time()
print('Part 2:', solve(input))
print(time.time() - start)
