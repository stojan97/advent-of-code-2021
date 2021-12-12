from collections import defaultdict


def get_input():
    graph = defaultdict(lambda: [])
    with open('input') as file:
        lines = [line.strip() for line in file]

        for line in lines:
            split = line.split('-')
            graph[split[0]].append(split[1])
            graph[split[1]].append(split[0])

    return graph


def dfs(cave, graph, visited):
    if cave == 'end':
        return 1

    if cave.islower():
        visited.add(cave)

    paths = 0
    for adj_cave in graph[cave]:
        if adj_cave not in visited:
            paths += dfs(adj_cave, graph, set(visited))

    return paths


def part1(graph):
    paths = dfs('start', graph, set())
    return paths


def dfs_twice_cave(cave, graph, visited, visited_twice):
    if cave == 'end':
        return 1

    if cave.islower():
        visited.add(cave)

    paths = 0
    for adj_cave in graph[cave]:

        if adj_cave in visited and not visited_twice and adj_cave.islower() and adj_cave not in ['start', 'end']:
            paths += dfs_twice_cave(adj_cave, graph, set(visited), True)

        if adj_cave not in visited:
            paths += dfs_twice_cave(adj_cave, graph, set(visited), visited_twice)

    return paths


def part2(graph):
    paths = dfs_twice_cave('start', graph, set(), False)
    return paths


graph = get_input()
print('Part 1:', part1(graph))
print('Part 2:', part2(graph))
