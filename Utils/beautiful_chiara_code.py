import itertools

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

def print_grid(known_grid, suggestion=None):
    for r in range(1, 6):
        row_str = []
        for c in range(1, 6):
            if (r, c) == suggestion:
                row_str.append(" X ")
            else:
                cell_val = known_grid[(r, c)]
                char = cell_val[0].upper() if cell_val != '?' else '.'
                row_str.append(f" {char} ")
        print("".join(row_str))

def solve_remaining_board(purples_tuple):
    # gets called when all 4 purples are known
    solved_board = {}
    for r in range(1, 6):
        for c in range(1, 6):
            if (r, c) in purples_tuple:
                solved_board[(r, c)] = 'purple/red'
            else:
                count = count_adjacent_purples(r, c, purples_tuple)
                for color, val in sphere_mines.items():
                    if val == count:
                        solved_board[(r, c)] = color
                        break
    return solved_board

def main():
    all_cells = [(r, c) for r in range(1, 6) for c in range(1, 6)]
    known_grid = {cell: '?' for cell in all_cells}
    possible_boards = list(itertools.combinations(all_cells, 4))

    while True:
        total_boards = len(possible_boards)
        if total_boards == 1:
            print("solved.")
            print_grid(known_grid)
            final_purples = possible_boards[0]
            solved_board = solve_remaining_board(final_purples)
            used_clicks = sum(1 for v in known_grid.values() if v not in ['?', 'purple'])
            clicks_left = 7 - used_clicks
            suggested_purples = []
            suggested_normals = []

            for cell, color in solved_board.items():
                if known_grid[cell] == '?':
                    if color == 'purple/red':
                        suggested_purples.append((cell, 1000, 'purple'))
                    else:
                        suggested_normals.append((cell, sphere_values[color], f"{color} ({sphere_values[color]} pts)"))

            normal_clicks_allowed = clicks_left
            if len(suggested_purples) > 0:
                normal_clicks_allowed -= 1

            suggested_normals.sort(key=lambda x: x[1], reverse=True)
            capped_normals = suggested_normals[:max(0, normal_clicks_allowed)]
            best_clicks = suggested_purples + capped_normals

            if clicks_left > 0:
                print(f"\n{clicks_left} {'click' if clicks_left == 1 else 'clicks'} left for:")
                for cell, val, description in best_clicks:
                    print(f"{cell[0]}, {cell[1]} -> {description}")
            else:
                print(f"\ngame over.")
            break

        elif total_boards == 0:
            print("\nalgorithm failed somewhere. may have hit an unlucky board. check if your solution has 7 teals haha")
            break

        purples_found = sum(1 for v in known_grid.values() if v == 'purple')

        if total_boards == 12650:
            suggestion = (4, 2)
            suggestion_text = "starting location: 4, 2."
        elif purples_found == 3:
            suggestion = None
            suggestion_text = "mudae has revealed the solution. click and report back."
        else:
            best_cell = None
            best_score = -1.0
            best_stats = (0, 0)
            guaranteed_purples = []

            unrevealed_cells = [cell for cell in all_cells if known_grid[cell] == '?']

            for c in unrevealed_cells:
                outcomes = {}
                for b in possible_boards:
                    res = 'purple' if c in b else count_adjacent_purples(c[0], c[1], b)
                    outcomes[res] = outcomes.get(res, 0) + 1

                p_purple = outcomes.get('purple', 0) / total_boards
                if p_purple == 1.0:
                    guaranteed_purples.append(c)

                gini = 1.0 - sum((count / total_boards) ** 2 for count in outcomes.values())
                score = p_purple + (0.1 * gini)

                if score > best_score:
                    best_score = score
                    best_cell = c
                    best_stats = (p_purple, gini)

            if guaranteed_purples:
                suggestion = guaranteed_purples[0]
                suggestion_text = f"{suggestion[0]}, {suggestion[1]} is 100% purple."
            else:
                suggestion = best_cell
                prob_pct = best_stats[0] * 100
                suggestion_text = (f"click {suggestion[0]}, {suggestion[1]}.\n"
                                   f"{prob_pct:.1f}% purple, {best_stats[1]*100:.3f}%+")

        print_grid(known_grid, suggestion)
        print(f"layouts: {total_boards}")
        print(suggestion_text)

        user_input = input("move: ").strip().lower()
        if user_input == 'q':
            break

        try:
            parts = user_input.replace(',', ' ').split()
            r, c = int(parts[0]), int(parts[1])
            color = parts[2]

            if (r, c) not in all_cells:
                print("coordinates must be between 1 and 5.")
                continue
            if color not in sphere_mines and color not in ['purple', 'red']:
                print(f"wrong colour. must be one of: {list(sphere_mines.keys()) + ['purple', 'red']}.")
                continue

            known_grid[(r, c)] = color
            new_boards = []
            for b in possible_boards:
                if color in ['purple', 'red']:
                    if (r, c) in b: new_boards.append(b)
                else:
                    if (r, c) not in b and count_adjacent_purples(r, c, b) == sphere_mines[color]:
                        new_boards.append(b)

            possible_boards = new_boards

        except (IndexError, ValueError):
            print("\nbad input.")


if __name__ == "__main__":
    main()