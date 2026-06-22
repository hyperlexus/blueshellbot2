import discord
from discord.ext.commands import slash_command, Cog
from discord import ApplicationContext, Option


one_hundred_percent_red = {
    (0,): 12,
        (0, 0): 25, (0, 0, -1): 41, (0, 0, -1, -1): 54,
        (0, 1): 15,
            (0, 1, 0): 52, (0, 1, 0, -1): 21,
            (0, 1, 1): 45, (0, 1, 1, -1): 14,
            (0, 1, 2): 45, (0, 1, 2, -1): 14,
            (0, 1, 4): 14,
        (0, 2): 14, (0, 2, -1): 52,
        (0, 3): 21, (0, 3, -1): 45,
    (1,): 23,
        (1, 0): 42,
            (1, 0, 0): 35,
                (1, 0, 0, 0): 11,
                (1, 0, 0, 1): 55,
                (1, 0, 0, 2): 55,
            (1, 0, 1): 51,
                (1, 0, 1, 0): 44,
                (1, 0, 1, 1): 31,
                (1, 0, 1, 2): 31,
                (1, 0, 1, 3): 15,
            (1, 0, 2): 44,
            (1, 0, 3): 31,
                (1, 0, 3, 0): 15,
                (1, 0, 3, 1): 51,
                (1, 0, 3, 2): 51,
        (1, 1): 32,
            (1, 1, 0): 53,
                (1, 1, 0, 0): 24,
                (1, 1, 0, 1): 13,
                (1, 1, 0, 2): 13,
            (1, 1, 1): 34,
                (1, 1, 1, 0): 22,
                (1, 1, 1, 1): 43,
                (1, 1, 1, 3): 43,
            (1, 1, 2): 34, (1, 1, 2, -1): 22,
            (1, 1, 3): 43,
            (1, 1, 4): 22,
        (1, 2): 53,
            (1, 2, 0): 22, (1, 2, 0, -1): 24,
            (1, 2, 1): 13, (1, 2, 1, -1): 43,
            (1, 2, 2): 13, (1, 2, 2, -1): 43,
            (1, 2, 4): 43,
        (1, 3): 32, (1, 3, -1): 34,
        (1, 4): 22, (1, 4, -1): 24, (1, 4, -1, -1): 13,
    (2,): 12,
        (2, 0): 53,
            (2, 0, 1): 31,
                (2, 0, 1, 0): 43,
                (2, 0, 1, 1): 35,
                (2, 0, 1, 2): 35,
            (2, 0, 2): 43,
            (2, 0, 3): 31, (2, 0, 3, -1): 35,
            (2, 0, 4): 43,
        (2, 1): 23,
            (2, 1, 1): 34,
                (2, 1, 1, 0): 13,
                (2, 1, 1, 1): 32,
                (2, 1, 1, 2): 32,
            (2, 1, 2): 13,
            (2, 1, 3): 34, (2, 1, 3, -1): 32,
            (2, 1, 4): 13,
        (2, 2): 32, (2, 2, -1): 13,
        (2, 3): 23, (2, 3, -1): 34,
        (2, 4): 13,
    (3,): 11,
        (3, 0): 24, (3, 0, -1): 42,
        (3, 1): 25,
            (3, 1, 0): 44, (3, 1, 0, -1): 51,
            (3, 1, 1): 22, (3, 1, 1, -1): 55,
            (3, 1, 2): 22, (3, 1, 2, -1): 55,
            (3, 1, 4): 15,
        (3, 2): 15, (3, 2, -1): 51,
        (3, 3): 55, (3, 3, -1): 22, (3, 3, -1, -1): 44,
    (4,): 23, (4, -1): 32, (4, -1, -1): 35, (4, -1, -1, -1): 43
}

geldfinder_strategy = {
    (0,): 35,
        (0, 0): 21,
            (0, 0, 0): 14,
            (0, 0, 1): 43,
                (0, 0, 1, 1): 23,
                (0, 0, 1, 2): 23,
                (0, 0, 1, 3): 54,
            (0, 0, 2): 23,
            (0, 0, 3): 54,
            (0, 0, 4): 11,
        (0, 1): 45,
            (0, 1, 0): 13,
            (0, 1, 1): 34, (0, 1, 1, -1): 25,
            (0, 1, 2): 25,
            (0, 1, 3): 34,
            (0, 1, 4): 55,
        (0, 2): 45,
            (0, 2, 1): 34, (0, 2, 1, -1): 25,
            (0, 2, 2): 25,
            (0, 2, 3): 34,
            (0, 1, 4): 55,
        (0, 3): 13,
        (0, 4): 25, (0, 4, -1): 34,
    (1,): 51,
        (1, 0): 45,
            (1, 0, 0): 22, (1, 0, -1): 32,
            (1, 0, 1): 11,
                (1, 0, 1, 0): 43,
                (1, 0, 1, 1): 44, (1, 0, 1, 1, 0): -1,
                (1, 0, 1, 2): 12,
                (1, 0, 1, 3): 44,
                (1, 0, 1, 4): 12,
            (1, 0, 2): 44, (1, 0, 2, -1): 43,
            (1, 0, 3): 12,
            (1, 0, 4): 45,
        (1, 1): 31,
            (1, 1, 0): 24,
            (1, 1, 3): 53,
        (1, 2): 31, (1, 2, -1): 53,
        (1, 3): 14,
            (1, 3, 1): 24,
            (1, 3, 2): 24,
            (1, 3, 4): 15, (1, 3, 4, -1): 24,
        (1, 4): 41, (1, 4, -1): 52,
    (2,): 45,
        (2, 0): 22,
            (2, 0, 1): 52, (2, 0, 1, -1): 32,
            (2, 0, 2): 52, (2, 0, 1, -1): 32,
            (2, 0, 4): 32,
        (2, 1): 44,
            (2, 1, 0): 12,
            (2, 1, 1): 41, (2, 1, 1, -1): 43,
            (2, 1, 2): 41, (2, 1, 1, -1): 43,
            (2, 1, 4): 43,
        (2, 2): 44,
            (2, 2, 1): 41, (2, 2, 1, -1): 43,
            (2, 2, 2): 41, (2, 2, 1, -1): 43,
            (2, 2, 4): 43,
        (2, 3): 12,
        (2, 4): 44,
    (3,): 53,
        (3, 0): 25,
            (3, 0, 1): 24,
            (3, 0, 2): 24,
            (3, 0, 4): 15, (3, 0, 4, -1): 24,
        (3, 1): 41,
            (3, 1, 1): 31,
            (3, 1, 2): 31,
            (3, 1, 4): 51, (3, 1, 4, -1): 31,
        (3, 2): 51,
        (3, 3): 31,
    (4,): 43,
        (4, 1): 41,
            (4, 1, 1): 32,
            (4, 1, 3): 52, (4, 1, 3, -1): 32,
        (4, 2): 41,
        (4, 3): 52, (4, 3, -1): 32,
}

sphere_values = {
    0: 10,
    1: 20,
    2: 35,
    3: 55,
    4: 90,
    5: 150
}

def get_next_click(what_has_been_clicked, strategy):
    click_sequence = tuple(what_has_been_clicked)
    if click_sequence in strategy:
        return strategy[click_sequence]

    b = list(what_has_been_clicked)
    for i in range(len(b)-1, 0, -1):
        b[i] = -1
        dings = tuple(b)

        if dings in strategy:
            return strategy[dings]
    return None

class RedfinderCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clicker = 0
        self.strategy_dict = {}

    @slash_command(name='redfinder', description='finds red, with different strategies.')
    async def redfinder(self, ctx: ApplicationContext,
                        strategy = Option(str, "what strategy to use", choices=["guaranteed red", "most value"], default="all")):
        match strategy:
            case "guaranteed red":
                strategy_dict = one_hundred_percent_red
                starting_click = "3, 3"
            case "most value":
                strategy_dict = geldfinder_strategy
                starting_click = "4, 2"
            case _:
                strategy_dict = geldfinder_strategy
                starting_click = "4, 2"
        view = AgainAndAgainButton(ctx.author.id, strategy_dict)
        await ctx.respond(f"This will help you make a lot of money from $oc. Please click at {starting_click} to start.\nCoordinates are Down, Right (for example, '1, 5' is top right).", view=view)

class AgainAndAgainButton(discord.ui.View):
    def __init__(self, who_has_clicked: int, strategy_dict: dict):
        super().__init__(timeout=120)
        self.what_has_been_clicked = []
        self.spawn()
        self.who_has_clicked = who_has_clicked
        self.strategy_dict = strategy_dict
        self.total_sphere_value = 0

    def spawn(self):
        colours = [
            ("Blue", 0, discord.ButtonStyle.primary, "🔵"),
            ("Teal", 1, discord.ButtonStyle.primary, "😢"),
            ("Green", 2, discord.ButtonStyle.primary, "🟢"),
            ("Yellow", 3, discord.ButtonStyle.primary, "🟡"),
            ("Orange", 4, discord.ButtonStyle.primary, "🟠"),
        ]

        for name, value, style, emote in colours:
            button = discord.ui.Button(label=name, style=style, emoji=emote, custom_id=f"colour_{value}")
            button.callback = self.something_has_been_clicked
            self.add_item(button)
        red_button = discord.ui.Button(label="Red", style=discord.ButtonStyle.success, emoji="<:spheres:1506804921444601913>", custom_id="colour_5", row=2)
        red_button.callback = self.something_has_been_clicked
        self.add_item(red_button)

    async def something_has_been_clicked(self, interaction: discord.Interaction):
        if interaction.user.id != self.who_has_clicked:
            return await interaction.response.send_message(
                "These are not your buttons. Please don't stick your nose in others' business, severus snape.",
                ephemeral=False
            )

        colour = int(interaction.custom_id.split("_")[1])
        self.total_sphere_value += sphere_values[colour]
        self.what_has_been_clicked.append(colour)
        stage = len(self.what_has_been_clicked)

        if self.what_has_been_clicked == [1, 0, 1, 1, 0] and self.strategy_dict == geldfinder_strategy:
            self.clear_items()
            await interaction.response.edit_message(
                content="that's crazy blud, you have hit the 0.023148% chance of hitting the single failing outcome."
                "you should complain about this.", view=self
            )
            return None

        if colour == 5:
            self.clear_items()
            await interaction.response.edit_message(
                content=f"Yay! You did it. +{self.total_sphere_value}<:spheres:1506804921444601913> (and the rest)", view=self
            )
            return None
        if stage >= 5:
            self.clear_items()
            await interaction.response.edit_message(
                content="ham gekackt.", view=self
            )
            return None

        next_move = get_next_click(self.what_has_been_clicked, self.strategy_dict)
        next_click = f"{str(next_move)[0]}, {str(next_move)[1]}"

        if next_move:
            msg = f"stage {stage+1}/5, please click at {next_click}."
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.clear_items()
            await interaction.response.edit_message(
                content=f"sie ham gelogen, diesen button kann es da ({self.what_has_been_clicked}) gar nicht geben!", view=self
            )
        return None

def setup(bot):
    bot.add_cog(RedfinderCog(bot))
