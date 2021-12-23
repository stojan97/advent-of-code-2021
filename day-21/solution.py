import operator
import re


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

        p1 = int(re.sub(r'[^-\d]', ' ', lines[0]).strip().split()[1])
        p2 = int(re.sub(r'[^-\d]', ' ', lines[1]).strip().split()[1])

    return p1, p2


def adjust(pos):
    return 10 if pos == 0 else pos


def part1(input):
    player_score = [[0, input[0]], [0, input[1]]]
    die_roll = 1
    turn = 0
    total_die_rolls = 1

    while True:
        player_score[turn][1] = adjust((player_score[turn][1] + 3 * die_roll + 3) % 10)
        player_score[turn][0] += player_score[turn][1]
        next_die_roll = (die_roll + 3) % 100
        if player_score[0][0] >= 1000 or player_score[1][0] >= 1000:
            total_die_rolls += 2
            break
        die_roll = 100 if next_die_roll == 0 else next_die_roll
        total_die_rolls += 3
        turn = (turn + 1) % 2

    winner = 0 if player_score[0][0] < player_score[1][0] else 1
    return player_score[winner][0] * total_die_rolls


def add(p1, p2, p3):
    init = list(map(operator.add, p1, p2))
    res = list(map(operator.add, init, p3))
    return res


def simulate_quantum_roll(scores, position_for, player, roll, memo):
    t = (scores[0], scores[1], position_for[0], position_for[1], player, roll)
    if t in memo:
        return memo[t]

    if scores[0] >= 21 or scores[1] >= 21:
        winner = 0 if scores[0] > scores[1] else 1
        wins = [0, 0]
        wins[winner] += 1
        memo[t] = wins
        return wins

    if roll == 4:
        scores[player] += position_for[player]
        res = simulate_quantum_roll(scores, position_for, (player + 1) % 2, 1, memo)
        memo[t] = res
        return res

    copy1_position = list(position_for)
    copy2_position = list(position_for)
    copy3_position = list(position_for)

    copy1_position[player] = adjust((copy1_position[player] + 1) % 10)
    copy2_position[player] = adjust((copy2_position[player] + 2) % 10)
    copy3_position[player] = adjust((copy3_position[player] + 3) % 10)

    split1 = simulate_quantum_roll(list(scores), copy1_position, player, roll + 1, memo)
    split2 = simulate_quantum_roll(list(scores), copy2_position, player, roll + 1, memo)
    split3 = simulate_quantum_roll(list(scores), copy3_position, player, roll + 1, memo)
    res = add(split1, split2, split3)

    memo[t] = res
    return res


def part2(input):
    p1_pos, p2_pos = input
    scores = [0, 0]
    memo = {}
    split1 = simulate_quantum_roll(scores, [adjust((p1_pos + 1) % 10), p2_pos], 0, 2, memo)
    split2 = simulate_quantum_roll(scores, [adjust((p1_pos + 2) % 10), p2_pos], 0, 2, memo)
    split3 = simulate_quantum_roll(scores, [adjust((p1_pos + 3) % 10), p2_pos], 0, 2, memo)
    wins = add(split1, split2, split3)

    return max(wins)


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
