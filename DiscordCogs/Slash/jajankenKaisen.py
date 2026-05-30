import discord
from discord.ext.commands import slash_command, Cog
from discord import ApplicationContext, player

from Config.Colors import BColors

who_beats_what = {
    "口": ["凤", "乾", "槓"],
    "凤": ["乾", "杖", "平"],
    "乾": ["杖", "槓", "吃"],
    "杖": ["槓", "平", "口"],
    "槓": ["平", "吃", "凤"],
    "平": ["吃", "口", "乾"],
    "吃": ["口", "凤", "杖"],
}

class HAAAAndView(discord.ui.View):
    def __init__(self, spiel, user_id: int):
        super().__init__(timeout=180)
        self.spiel = spiel
        self.user_id = user_id
        self.mach_buttons()

    def mach_buttons(self):
        hand = self.spiel.hands[self.user_id]
        unique_cards = set(hand)
        for card in who_beats_what.keys():
            if card in unique_cards:
                count = hand.count(card)
                button_blud = discord.ui.Button(
                    label=f"{card} x{count}",
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"card_{card}_{self.user_id}",
                )
                button_blud.callback = self.card_ausgewaehlt
                self.add_item(button_blud)

    async def card_ausgewaehlt(self, interaction: discord.Interaction):
        card = interaction.custom_id.split("_")[1]
        await self.spiel.accept_choice(self.user_id, card, interaction) # kommt noch

class WantToPlay(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=60)
        self.player1 = player1
        self.player2 = player2
        self.__colors = BColors()

    @discord.ui.button(label="ja", style=discord.ButtonStyle.success)
    async def ja_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.player2.id:
            return await interaction.response.send_message(
                "these are not your buttons, please do not stick your nose in others' business severus snape"
            )

        spiel = Spiel(self.player1, self.player2)
        embed = discord.Embed(
            title="Jajanken",
            description=f"{self.player1.mention} vs {self.player2.mention}",
            color=self.__colors.GREEN
        )
        embed.add_field(name=f"{self.player1.display_name}'s cards", value="7")
        embed.add_field(name=f"{self.player2.display_name}'s cards", value="7")

        await interaction.response.edit_message(content=None, embed=embed, view=spiel)

        spiel.game_ongoing = interaction.message


class Spiel(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=None)
        self.player1 = player1
        self.player2 = player2
        self.__colors = BColors()
        base_hand = ["口", "凤", "杖", "平", "吃", "槓", "乾"]

        self.hands = {
            player1.id: base_hand.copy(),
            player2.id: base_hand.copy()
        }
        self.choices = {player1.id: None, player2.id: None}
        self.game_ongoing = None

        self.is_geeking = False

        choose_card_button = discord.ui.Button(label="chews food", style=discord.ButtonStyle.primary)
        choose_card_button.callback = self.show_hand
        self.add_item(choose_card_button)

        exit_button = discord.ui.Button(label="exit", style=discord.ButtonStyle.danger)
        exit_button.callback = self.exit_game
        self.add_item(exit_button)

        repost_button = discord.ui.Button(label="embed runterholen", style=discord.ButtonStyle.success)
        repost_button.callback = self.repost_game
        self.add_item(repost_button)

    async def show_hand(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.player1.id, self.player2.id]:
            return await interaction.response.send_message(
                "these are not your buttons, please do not stick your nose in others' business severus snape"
            )

        if self.choices.get(interaction.user.id) is not None:
            return await interaction.response.send_message(
                "you have already plate. please wait for the other snoozemaxxer to play!"
            )

        hand = self.hands[interaction.user.id]

        hand_view = HAAAAndView(self, interaction.user.id)
        await interaction.response.send_message("select card", view=hand_view, ephemeral=True)
        return None

    async def accept_choice(self, user_id: int, card: str, interaction: discord.Interaction):
        if self.is_geeking: return
        user_id = int(user_id)
        self.choices[user_id] = card
        has_player1_playad = self.choices.get(self.player1.id) is not None
        has_player2_playad = self.choices.get(self.player2.id) is not None

        if has_player1_playad and has_player2_playad:
            self.is_geeking = True

        try:
            await interaction.response.edit_message(content=f"you played {card}", view=None)
        except discord.NotFound:
            pass

        if has_player1_playad and has_player2_playad:
            await self.calculate_outcome()
        else:
            player1_dingens = "locked in" if has_player1_playad else "geeked"
            player2_dingens = "locked in" if has_player2_playad else "geeked"

            embed = discord.Embed(
                title="Jajanken",
                description="waiting for both players to play",
                color=self.__colors.BLUE
            )
            embed.add_field(name=self.player1.display_name, value=player1_dingens)
            embed.add_field(name=self.player2.display_name, value=player2_dingens)

            if self.game_ongoing:
                await self.game_ongoing.edit(embed=embed, view=self)

    async def calculate_outcome(self):
        if not self.game_ongoing: return

        card1 = self.choices[self.player1.id]
        card2 = self.choices[self.player2.id]
        self.choices = {self.player1.id: None, self.player2.id: None}

        if card1 == card2:
            result_text = f"both players have played {card2}, it's a zeichnung."
        elif card2 in who_beats_what.get(card1, []):
            result_text = (f"{self.player1.display_name} plaid {card1}, beats {self.player2.display_name} who plaid {card2}.\n"
                           f"{self.player1.display_name} gains {card2}.")
            if card2 in self.hands[self.player2.id]:
                self.hands[self.player2.id].remove(card2)
            self.hands[self.player1.id].append(card2)
        else:
            result_text = (f"{self.player2.display_name} plaid {card2}, beats {self.player1.display_name} who plaid {card1}.\n"
                           f"{self.player2.display_name} gains {card1}.")
            if card1 in self.hands[self.player1.id]:
                self.hands[self.player1.id].remove(card1)
            self.hands[self.player2.id].append(card1)

        player1_count = len(self.hands[self.player1.id])
        player2_count = len(self.hands[self.player2.id])

        if player1_count == 0 or player2_count == 0:
            weiner = self.player1 if player2_count == 0 else self.player2
            embed = discord.Embed(
                title="resalt",
                description=f"{result_text}\n\n{weiner.display_name} weins.",
                colour=self.__colors.GREEN,
            )
            await self.game_ongoing.edit(embed=embed, view=self)
            return

        embed = discord.Embed(
            title="resalt",
            description=f"{result_text}",
            colour=self.__colors.BLUE,
        )
        embed.add_field(name=f"{self.player1.display_name}'s cards", value=str(player1_count))
        embed.add_field(name=f"{self.player2.display_name}'s cards", value=str(player2_count))

        await self.game_ongoing.edit(embed=embed, view=self)
        self.is_geeking = False

    async def exit_game(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.player1.id, self.player2.id]:
            return await interaction.response.send_message(
                "these are not your buttons, please do not stick your nose in others' business severus snape"
            )
        self.clear_items()
        embed = discord.Embed(
            title="game over",
            description=f"{interaction.user.display_name} has rage quit. what a spast.",
            colour=self.__colors.RED
        )
        await interaction.response.edit_message(embed=embed, view=self)

        self.stop()
        return None

    async def repost_game(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.player1.id, self.player2.id]:
            return await interaction.response.send_message(
                "these are not your buttons, please do not stick your nose in others' business severus snape"
            )
        await interaction.response.defer()
        current_embed = interaction.message.embeds[0]
        if self.game_ongoing:
            try:
                await self.game_ongoing.delete()
            except discord.NotFound:
                return await interaction.response.send_message("blart jemand hats schon gelöl während sie gedrückt ham")
        new_embed = await interaction.channel.send(embed=current_embed, view=self)
        self.game_ongoing = new_embed

class JajankenCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='jajanken', description='カアド', guild_ids=[995966314877300737])
    async def jajanken(self, ctx: ApplicationContext, opponent: discord.Member):
        if opponent.bot:
            return await ctx.respond("cannot play against a bot")
        if opponent.id == ctx.author.id:
            return await ctx.respond("blud ist ein einsamer spast")

        view = WantToPlay(ctx.author, opponent)
        await ctx.respond(
            f"{opponent.mention}, {ctx.author.display_name} is calling, do you accept?", view=view
        )

def setup(bot):
    bot.add_cog(JajankenCog(bot))
