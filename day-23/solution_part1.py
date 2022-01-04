import time
from collections import deque
from copy import copy
from heapq import *


class Amphipod:

    def __init__(self, idx, type, home_nodes, energy) -> None:
        self.idx = idx
        self.type = type
        self.home_nodes = home_nodes
        self.energy = energy

    def __repr__(self) -> str:
        return f'Amphipod (idx={self.idx}, type={self.type}, home_nodes={self.home_nodes}, energy={self.energy})'

    def is_home(self, amphipods_location: dict):
        return amphipods_location[self.idx] in self.home_nodes


class State:

    def __init__(self, total_energy, amphipod, occupied_by) -> None:
        self.total_energy = total_energy
        self.amphipod = amphipod
        self.occupied_by = occupied_by

    def __lt__(self, other: 'State'):
        return self.total_energy < other.total_energy

    def __repr__(self) -> str:
        return f'State (current_amphipod={self.amphipod}, occupied_by={self.occupied_by}'

    def __eq__(self, o: 'State') -> bool:
        return self.amphipod == o.amphipod and self.occupied_by == o.occupied_by

    def __hash__(self) -> int:
        occupied_by_items = tuple(sorted(self.occupied_by.items()))
        return hash((self.amphipod, occupied_by_items))


def add_edge(first, second, nodes):
    nodes[first].append(second)
    nodes[second].append(first)


def invert_dict(occupied_by: dict):
    return {v: k for k, v in occupied_by.items()}


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    lines[3] = '##' + lines[3]

    bot_row = ''.join(filter(str.isalpha, lines[3]))
    top_row = ''.join(filter(str.isalpha, lines[2]))

    nodes = [[] for _ in range(19)]
    g_index = 0
    amphipods = []
    energy = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    home = {
        'A': [0, 1],
        'B': [2, 3],
        'C': [4, 5],
        'D': [6, 7]
    }
    for index in range(len(bot_row)):
        bot_cell = bot_row[index]
        top_cell = top_row[index]

        bot = Amphipod(g_index, bot_cell, home[bot_cell], energy[bot_cell])
        top = Amphipod(g_index + 1, top_cell, home[top_cell], energy[top_cell])

        amphipods += [bot, top]
        add_edge(g_index, g_index + 1, nodes)
        g_index += 2

    next_room = 1

    for index in range(8, 19):

        if index not in [8, 18] and index % 2 == 0:
            add_edge(index, next_room, nodes)
            next_room += 2

        if index != 8:
            add_edge(index, index - 1, nodes)

    return amphipods, nodes


def all_covered(amphipods, amphipods_location):
    return all(amphipod.is_home(amphipods_location) for amphipod in amphipods)


def get_covered(amphipods, amphipods_location):
    return sum(amphipod.is_home(amphipods_location) for amphipod in amphipods)


def are_all_stacked(amphipods, start, limit, occupied_by, add, amphipods_location):
    if start == limit:
        return True

    return all(node in occupied_by and amphipods[occupied_by[node]].is_home(amphipods_location) for node in range(start, limit + add))


SKIP_ROOMS = {10, 12, 14, 16} | {i for i in range(8)}
TOP_ROOMS = {8, 9, 11, 13, 15, 17, 18}


def get_possible_next_nodes(nodes, amphipod_idx, occupied_by, amphipods, amphipods_location):
    start_location = amphipods_location[amphipod_idx]
    home_nodes = amphipods[amphipod_idx].home_nodes
    amphipod_energy = amphipods[amphipod_idx].energy
    h_nodes_set = set(home_nodes)

    stacked_same_kind = start_location in h_nodes_set and are_all_stacked(amphipods, home_nodes[0], start_location, occupied_by, 1, amphipods_location)

    if stacked_same_kind:
        return {}

    dist = {}
    q = deque([(start_location, 0)])

    visited = set(occupied_by.keys())
    to_skip = set(SKIP_ROOMS)
    to_skip.difference_update(h_nodes_set)

    while q:
        next_node, energy = q.popleft()
        energy_so_far = energy + amphipod_energy

        for node in nodes[next_node]:
            if node not in visited:
                if node not in to_skip:
                    dist[node] = energy_so_far
                visited.add(node)
                q.append((node, energy_so_far))

    first_home_node = next(filter(lambda n: n in dist, home_nodes), None)

    if first_home_node is not None and are_all_stacked(amphipods, home_nodes[0], first_home_node, occupied_by, 0, amphipods_location):
        return {first_home_node: dist[first_home_node]}

    # amphipod was locked
    if start_location in TOP_ROOMS:
        return {}

    for home_node in home_nodes:
        if home_node in dist:
            dist.pop(home_node)

    return dist


def solve(input):
    amphipods, nodes = input
    print(*amphipods, sep='\n')
    print(*nodes, sep='\n')
    pq = []
    heapify(pq)
    occupied_by = {i: i for i in range(8)}

    for i in range(1, 8, 2):
        st = (State(0, i, copy(occupied_by)))
        heappush(pq, st)

    c = 0

    memo = set()

    while pq:
        state = heappop(pq)
        total_energy = state.total_energy
        amphipod_idx = state.amphipod
        current_occupied_by = state.occupied_by
        amphipods_location = invert_dict(current_occupied_by)
        amphipod_location = amphipods_location[amphipod_idx]

        if state in memo:
            continue

        memo.add(state)

        covered = get_covered(amphipods, amphipods_location)
        if c % 10000 == 0:
            print(f'Covered: {covered}, energy={total_energy}, count={c}')

        c += 1

        if all_covered(amphipods, amphipods_location):
            print(f'Covered: {covered}, energy={total_energy}, count={c}')
            return total_energy

        possible_next_nodes = get_possible_next_nodes(nodes, amphipod_idx, current_occupied_by, amphipods, amphipods_location)

        for next_node, energy in possible_next_nodes.items():
            next_energy = total_energy + energy
            next_occupied_by = copy(current_occupied_by)
            next_occupied_by.pop(amphipod_location)
            next_occupied_by[next_node] = amphipod_idx

            for idx, _ in enumerate(amphipods):
                if idx != amphipod_idx:
                    new_state = State(next_energy, idx, next_occupied_by)
                    heappush(pq, new_state)

    return -1


input = get_input()
start = time.time()
# around 20 seconds for inputs with a lot of arrangements
# TODO: amphipods list can be passed as a reference
print('Part 1:', solve(input))
print(time.time() - start)
