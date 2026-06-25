import itertools
import random
import time

sphere_values = {
    'purple': 5,
    'blue': 10,
    'teal': 20,
    'green': 35,
    'yellow': 55,
    'orange': 90,
    'red': 150
}
sphere_mines = {
    'blue': 0,
    'teal': 1,
    'green': 2,
    'yellow': 3,
    'orange': 4
}

all_cells = [(r, c) for r in range(1, 6) for c in range(1, 6)]
all_possible_boards = list(itertools.combinations(all_cells, 4))

def helper_get_adjacent_cells(r, c):
    adj = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 1 <= nr <= 5 and 1 <= nc <= 5:
                adj.append((nr, nc))
    return adj

def count_adjacent_purples(r, c, purples_tuple):
    return sum(1 for cell in helper_get_adjacent_cells(r, c) if cell in purples_tuple)

def get_cell_color(r, c, secret_mines, purples_found):
    if (r, c) in secret_mines:
        return 'purple' if purples_found < 3 else 'red'
    else:
        count = count_adjacent_purples(r, c, secret_mines)
        for color, val in sphere_mines.items():
            if val == count:
                return color
        return None

def solve_remaining_board(secret_mines):
    solved_board = {}
    for r in range(1, 6):
        for c in range(1, 6):
            if (r, c) in secret_mines:
                solved_board[(r, c)] = 'mine'
            else:
                count = count_adjacent_purples(r, c, secret_mines)
                for color, val in sphere_mines.items():
                    if val == count:
                        solved_board[(r, c)] = color
                        break
    return solved_board

def simulate_game():
    secret_mines = random.choice(all_possible_boards)
    known_grid = {cell: '?' for cell in all_cells}
    possible_boards = all_possible_boards[:]

    clicks_used = 0
    score = 0
    purples_found = 0
    red_found = False

    while True:
        total_boards = len(possible_boards)
        if total_boards == 0:
            return score, False, clicks_used

        if total_boards == 1 or purples_found == 3:
            clicks_left = 7 - clicks_used
            solved_board = solve_remaining_board(secret_mines)

            unclicked_mines = [cell for cell in secret_mines if known_grid[cell] == '?']
            for i, mine_cell in enumerate(unclicked_mines):
                if purples_found < 3:  # free purple
                    score += sphere_values['purple']
                    purples_found += 1
                    known_grid[mine_cell] = 'purple'
                else:
                    if clicks_left > 0:
                        score += sphere_values['red']
                        clicks_left -= 1
                        red_found = True
                        known_grid[mine_cell] = 'red'
            suggested_normals = []
            for cell, color in solved_board.items():
                if known_grid[cell] == '?' and color != 'mine':
                    suggested_normals.append(sphere_values[color])

            suggested_normals.sort(reverse=True)
            score += sum(suggested_normals[:max(0, clicks_left)])
            clicks_used += (7 - clicks_used) - clicks_left  # Update for tracking

            return score, red_found, clicks_used
        if clicks_used >= 7:
            return score, red_found, clicks_used
        if total_boards == 12650:
            best_cell = (4, 2)
        else:
            best_cell = None
            best_score = -1.0

            unrevealed_cells = [cell for cell in all_cells if known_grid[cell] == '?']
            for c in unrevealed_cells:
                outcomes = {}
                for b in possible_boards:
                    res = 'purple' if c in b else count_adjacent_purples(c[0], c[1], b)
                    outcomes[res] = outcomes.get(res, 0) + 1

                p_purple = outcomes.get('purple', 0) / total_boards
                if p_purple == 1.0:
                    best_cell = c
                    break

                gini = 1.0 - sum((count / total_boards) ** 2 for count in outcomes.values())
                cell_score = p_purple + (0.1 * gini)

                if cell_score > best_score:
                    best_score = cell_score
                    best_cell = c
        r, c = best_cell
        color = get_cell_color(r, c, secret_mines, purples_found)

        known_grid[(r, c)] = color
        score += sphere_values[color]

        if color != 'purple':
            clicks_used += 1
        else:
            purples_found += 1
        new_boards = []
        for b in possible_boards:
            if color in ['purple', 'red']:
                if (r, c) in b: new_boards.append(b)
            else:
                if (r, c) not in b and count_adjacent_purples(r, c, b) == sphere_mines[color]:
                    new_boards.append(b)
        possible_boards = new_boards


def main():
    games = 100
    print(f"simulating {games} games")
    start_time = time.time()

    total_score = 0
    wins = 0
    total_clicks = 0
    scores = []

    for i in range(1, games + 1):
        score, won, clicks = simulate_game()
        total_score += score
        total_clicks += clicks
        scores.append(score)
        if won:
            wins += 1

        if i % 100 == 0:
            print(f"{i}/{games} done")

    end_time = time.time()

    print("\nsimulation done. results:")
    print(f"time elapsed:      {(end_time - start_time)*9:.2f} seconds")
    print(f"win rate:          {(wins / games) * 100:.2f}%")
    print(f"avg score per $oq:  {total_score / games:.1f} pts")
    print(f"max score (/485):  {max(scores)} pts")
    print(f"minimum score:     {min(scores)} pts")


if __name__ == "__main__":
    main()