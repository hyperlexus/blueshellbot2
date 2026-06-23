import discord
from discord.ext.commands import slash_command, Cog
from discord import ApplicationContext
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

def solve_remaining_board(purples_tuple):
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


class OqSolverView(discord.ui.View):
    def __init__(self, who_has_clicked: int):
        super().__init__(timeout=300)
        self.who_has_clicked = who_has_clicked
        self.clicks_used = 0

        self.all_cells = [(r, c) for r in range(1, 6) for c in range(1, 6)]
        self.known_grid = {cell: '?' for cell in self.all_cells}
        self.possible_boards = list(itertools.combinations(self.all_cells, 4))

        self.current_suggestion = (4, 2)
        self.spawn_color_buttons()

    def spawn_color_buttons(self):
        self.clear_items()

        row1_colors = [
            ("Blue", "blue", discord.ButtonStyle.primary, "🔵"),
            ("Teal", "teal", discord.ButtonStyle.primary, "😢"),
            ("Green", "green", discord.ButtonStyle.primary, "🟢"),
            ("Yellow", "yellow", discord.ButtonStyle.primary, "🟡"),
            ("Orange", "orange", discord.ButtonStyle.primary, "🟠"),
        ]
        for name, value, style, emote in row1_colors:
            button = discord.ui.Button(label=name, style=style, emoji=emote, custom_id=f"color_{value}", row=0)
            button.callback = self.process_turn
            self.add_item(button)

        row2_colors = [
            ("Purple", "purple", discord.ButtonStyle.secondary, "🟣"),
            ("Red", "red", discord.ButtonStyle.success, "<:spheres:1506804921444601913>")
        ]
        for name, value, style, emote in row2_colors:
            button = discord.ui.Button(label=name, style=style, emoji=emote, custom_id=f"color_{value}", row=1)
            button.callback = self.process_turn
            self.add_item(button)

    async def process_turn(self, interaction: discord.Interaction):
        if interaction.user.id != self.who_has_clicked:
            return await interaction.response.send_message("Messrs Moony, Wormtail, Padfoot and Prongs offer their "
            "compliments to Professor Snape, and request that he keep his abnormally large nose out of other people's business.")

        color_clicked = interaction.custom_id.split("_")[1]

        if color_clicked != 'purple':
            self.clicks_used += 1

        r, c = self.current_suggestion
        self.known_grid[(r, c)] = color_clicked

        new_boards = []
        for b in self.possible_boards:
            if color_clicked in ['purple', 'red']:
                if (r, c) in b: new_boards.append(b)
            else:
                if (r, c) not in b and count_adjacent_purples(r, c, b) == sphere_mines[color_clicked]:
                    new_boards.append(b)
        self.possible_boards = new_boards
        total_boards = len(self.possible_boards)

        if total_boards == 0:
            self.clear_items()
            return await interaction.response.edit_message(
                content="impossible board! you probably misclicked.", view=self)

        if total_boards == 1:
            return await self.handle_solved_board(interaction)

        purples_found = sum(1 for v in self.known_grid.values() if v in ['purple', 'red'])
        if purples_found == 3:
            return await self.ask_for_missing_purple(interaction)

        if self.clicks_used >= 7:
            self.clear_items()
            return await interaction.response.edit_message(
                content=f"💀 ham gekackt. all clicks gone, but {total_boards} possible layouts remaining. belaal.",
                view=self
            )

        unrevealed_cells = [cell for cell in self.all_cells if self.known_grid[cell] == '?']
        best_cell = None
        best_score = -1.0
        best_prob = 0.0

        for cell in unrevealed_cells:
            outcomes = {}
            for b in self.possible_boards:
                res = 'purple' if cell in b else count_adjacent_purples(cell[0], cell[1], b)
                outcomes[res] = outcomes.get(res, 0) + 1

            p_purple = outcomes.get('purple', 0) / total_boards
            if p_purple == 1.0:
                best_cell = cell
                best_prob = 100.0
                break

            gini = 1.0 - sum((count / total_boards) ** 2 for count in outcomes.values())
            score = p_purple + (0.1 * gini)

            if score > best_score:
                best_score = score
                best_cell = cell
                best_prob = p_purple * 100

        self.current_suggestion = best_cell

        if best_prob == 100.0:
            msg = f"remaining possible layouts: {total_boards}\n\nPlease click **{best_cell[0]}, {best_cell[1]}**. (100% purple).\nhit the purple colour button afterwards:"
        else:
            msg = f"remaining possible layouts: {total_boards}\n\nclick on {best_cell[0]}, {best_cell[1]}. ({best_prob:.1f}% purple).\ninput its colour below:"

        await interaction.response.edit_message(content=msg, view=self)
        return None

    async def ask_for_missing_purple(self, interaction: discord.Interaction):
        self.clear_items()

        possible_purple_cells = {c for b in self.possible_boards for c in b if self.known_grid[c] == '?'}

        row, col = 0, 0
        for r, c in sorted(possible_purple_cells):
            button = discord.ui.Button(label=f"{r}, {c}", style=discord.ButtonStyle.secondary,
                                       custom_id=f"coord_{r}_{c}", row=row)
            button.callback = self.process_missing_purple
            self.add_item(button)

            col += 1
            if col == 5:
                col = 0
                row += 1

        msg = "the red has been found!\n\nuse the buttons to relay the information on where it is."
        await interaction.response.edit_message(content=msg, view=self)

    async def process_missing_purple(self, interaction: discord.Interaction):
        if interaction.user.id != self.who_has_clicked:
            return

        parts = interaction.custom_id.split("_")
        r, c = int(parts[1]), int(parts[2])

        self.clicks_used += 1
        self.known_grid[(r, c)] = 'red'

        self.possible_boards = [b for b in self.possible_boards if (r, c) in b]

        if len(self.possible_boards) == 1:
            await self.handle_solved_board(interaction)
        else:
            await interaction.response.edit_message(
                content="internal error, coordinate doesn't match.", view=None)

    async def handle_solved_board(self, interaction: discord.Interaction):
        self.clear_items()
        clicks_left = 7 - self.clicks_used

        # if board is solved and no clicks are left.
        if clicks_left <= 0:
            if 'red' in self.known_grid.values():
                return await interaction.response.edit_message(
                    content="game completed by clicking the red sphere as your last click.",
                    view=None
                )
            else:
                return await interaction.response.edit_message(
                    content="💀 game over! board is solved, but there are no more clicks left. belaal.",
                    view=None
                )

        final_purples = self.possible_boards[0]
        solved_board = solve_remaining_board(final_purples)

        unrevealed_mines = []
        suggested_normals = []

        for cell, color in solved_board.items():
            if self.known_grid[cell] == '?':
                if color == 'purple/red':
                    unrevealed_mines.append(cell)
                else:
                    val = sphere_values[color]
                    suggested_normals.append((cell, val, f"**{color}** ({val} pts)"))

        suggested_normals.sort(key=lambda x: x[1], reverse=True)
        formatted_mines = []
        red_clicks_cost = 0

        for i, cell in enumerate(unrevealed_mines):
            if i < len(unrevealed_mines) - 1:
                formatted_mines.append((cell, 1000, '**purple** (free)'))
            else:
                formatted_mines.append((cell, 1000, '**red** (150pts)'))
                red_clicks_cost = 1

        normal_clicks_allowed = clicks_left - red_clicks_cost
        capped_normals = suggested_normals[:max(0, normal_clicks_allowed)]

        best_clicks = formatted_mines + capped_normals

        if best_clicks:
            clicks_str = "\n".join([f"{cell[0]}, {cell[1]}: {desc}" for cell, val, desc in best_clicks])
            msg = f"board solved, you have **{clicks_left} clicks** remaining.\n\nclick these squares to spheremaxx:\n\n{clicks_str}"
        else: msg = "board solved, but no clicks left. smth might have gone wrong internally or you misclicked."

        await interaction.response.edit_message(content=msg, view=None)
        return None

class MinefinderCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='minefinder', description='mudae $oq solver')
    async def minefinder(self, ctx: ApplicationContext):
        view = OqSolverView(ctx.author.id)
        await ctx.respond((
            "first, click at 4, 2.\n"
            "*(Coordinates are Down, Right. For example, '1, 5' is top right.)*\n\n"
            "use the buttons to relay the feedback given."
        ), view=view)


def setup(bot):
    bot.add_cog(MinefinderCog(bot))