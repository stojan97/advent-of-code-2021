import time
from collections import deque
from copy import copy, deepcopy
from heapq import *


class Amphipod:

    def __init__(self, type, node_index, home_nodes, energy) -> None:
        self.type = type
        self.node_index = node_index
        self.home_nodes = home_nodes
        self.energy = energy
        self.locked = False

    def __repr__(self) -> str:
        return f'Amphipod (type={self.type}, node_index={self.node_index}, home_nodes={self.home_nodes}, energy={self.energy})'

    def is_home(self):
        return self.node_index in self.home_nodes


class State:

    def __init__(self, total_energy, amphipod, amphipods, occupied_by) -> None:
        self.total_energy = total_energy
        self.amphipod = amphipod
        self.actual_amphipod = amphipods[amphipod]
        self.amphipods = amphipods
        self.occupied_by = occupied_by

    def __lt__(self, other: 'State'):
        return self.total_energy < other.total_energy

    def __repr__(self) -> str:
        return f'State (current_amphipod={self.amphipod}, amphipods={len(self.amphipods)}, occupied_by={self.occupied_by}, AMPHIPOD={self.actual_amphipod})'

    def __eq__(self, o: 'State') -> bool:
        return self.amphipod == o.amphipod and self.occupied_by == o.occupied_by

    def __hash__(self) -> int:
        occupied_by_items = tuple(sorted(self.occupied_by.items()))
        return hash((self.amphipod, occupied_by_items))


def add_edge(first, second, nodes):
    nodes[first].append(second)
    nodes[second].append(first)


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

        bot = Amphipod(bot_cell, g_index, home[bot_cell], energy[bot_cell])
        top = Amphipod(top_cell, g_index + 1, home[top_cell], energy[top_cell])

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


def all_covered(amphipods):
    return all(amphipod.is_home() for amphipod in amphipods)


def get_covered(amphipods):
    return sum(amphipod.is_home() for amphipod in amphipods)


def are_all_stacked(amphipods, start, limit, occupied_by, add):
    if start == limit:
        return True

    return all(node in occupied_by and amphipods[occupied_by[node]].is_home() for node in range(start, limit + add))


SKIP_ROOMS = {10, 12, 14, 16} | {i for i in range(8)}


def get_possible_next_nodes(nodes, amphipod, occupied_by, amphipods):
    node_index = amphipod.node_index
    home_nodes = amphipod.home_nodes
    h_nodes_set = set(home_nodes)

    stacked_same_kind = node_index in h_nodes_set and are_all_stacked(amphipods, home_nodes[0], node_index, occupied_by, 1)

    if stacked_same_kind:
        return {}

    dist = {}
    q = deque([(amphipod.node_index, 0)])

    visited = set(occupied_by.keys())
    to_skip = set(SKIP_ROOMS)
    to_skip.difference_update(h_nodes_set)

    while q:
        next_node, energy = q.popleft()
        energy_so_far = energy + amphipod.energy

        for node in nodes[next_node]:
            if node not in visited:
                if node not in to_skip:
                    dist[node] = energy_so_far
                visited.add(node)
                q.append((node, energy_so_far))

    first_home_node = next(filter(lambda n: n in dist, home_nodes), None)

    if first_home_node is not None and are_all_stacked(amphipods, home_nodes[0], first_home_node, occupied_by, 0):
        return {first_home_node: dist[first_home_node]}

    if amphipod.locked:
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
        st = (State(0, i, amphipods, copy(occupied_by)))
        heappush(pq, st)

    c = 0

    memo = set()

    while pq:
        state = heappop(pq)
        total_energy = state.total_energy
        current_amphipod = state.amphipods[state.amphipod]
        current_amphipods = state.amphipods
        current_occupied_by = state.occupied_by

        if state in memo:
            continue

        memo.add(state)

        covered = get_covered(current_amphipods)
        if c % 10000 == 0:
            print(f'Covered: {covered}, energy={total_energy}, count={c}')

        c += 1

        if all_covered(current_amphipods):
            print(f'Covered: {covered}, energy={total_energy}, count={c}')
            return total_energy

        possible_next_nodes = get_possible_next_nodes(nodes, current_amphipod, current_occupied_by, current_amphipods)

        for next_node, energy in possible_next_nodes.items():
            next_energy = total_energy + energy
            next_amphipods = deepcopy(current_amphipods)
            next_occupied_by = copy(current_occupied_by)
            next_amphipod = next_amphipods[state.amphipod]
            next_occupied_by.pop(next_amphipod.node_index)
            next_amphipod.node_index = next_node
            next_amphipod.locked = True
            next_occupied_by[next_node] = state.amphipod

            for idx, _ in enumerate(next_amphipods):
                if idx != state.amphipod:
                    new_state = State(next_energy, idx, next_amphipods, next_occupied_by)
                    heappush(pq, new_state)

    return -1


input = get_input()
start = time.time()
# around 46 seconds for inputs with a lot of arrangements
# TODO: amphipods list can be passed as a reference
print('Part 1:', solve(input))
print(time.time() - start)
