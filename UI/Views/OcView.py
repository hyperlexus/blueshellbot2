import random
import discord

VALUE_MAP = {
    "blue": 10,
    "teal": 20,
    "green": 35,
    "yellow": 55,
    "orange": 90,
    "red": 150,
}

EMOJI_MAP = {
    "blue": "<:spB:1543315566939476068>",
    "teal": "<:spT:1543315783105515581>",
    "green": "<:spG:1543315593661513748>",
    "yellow": "<:spY:1543315622103093328>",
    "orange": "<:spO:1543315669872025641>",
    "red": "<:sp:1543315693989003264>",
    "unrevealed": "<:spU:1543316207141257296>"
}


class OcGameView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.current_score = 0
        self.clicks_remaining = 5
        self.game_active = True
        self.grid_data = []
        self.what_has_been_clicked = []
        self.log_message = None
        red_place = random.choice([i for i in range(25) if i != 12])
        rx, ry = red_place % 5, red_place // 5

        kings, bishops, goofy_coordinates, blues = [], [], [], []
        # kp mehr was goofy coordinates ist und wie die ganze scheiße hier funktioniert lmao
        for i in range(25):
            if i == red_place: continue
            x, y = i % 5, i // 5
            dx, dy = abs(x - rx), abs(y - ry)
            if dx + dy == 1: kings.append(i)
            elif dx == dy: bishops.append(i)
            elif dx == 0 or dy == 0: goofy_coordinates.append(i)
            else: blues.append(i)

        random.shuffle(kings)
        oranges = kings[:2]
        unused_kings = kings[2:]

        random.shuffle(bishops)
        yellows = bishops[:3]
        unused_bishops = bishops[3:]

        possible_rooks = goofy_coordinates + unused_kings
        random.shuffle(possible_rooks)
        greens = possible_rooks[:4]
        unused_rooks = possible_rooks[4:]

        teals = unused_bishops + unused_rooks
        temp_data = [None] * 25

        def assign(indices, color):
            for i in indices:
                temp_data[i] = color

        assign([red_place], "red")
        assign(oranges, "orange")
        assign(yellows, "yellow")
        assign(greens, "green")
        assign(teals, "teal")
        assign(blues, "blue")

        for i in range(25):
            self.grid_data.append({"color": temp_data[i], "revealed": False, "value": VALUE_MAP[temp_data[i]]})

        for row in range(5):
            for column in range(5):
                index = (row * 5) + column
                button = discord.ui.Button(
                    emoji=EMOJI_MAP["unrevealed"],
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"oc_{index}",
                    row=row,
                )
                button.callback = self.callback2(index)
                self.add_item(button)

    def i_have_a_big_log(self, done: bool=False):
        lines = []
        for color, val in self.what_has_been_clicked:
            emoji = EMOJI_MAP[color]
            lines.append(f"{emoji} **+{val}**")

        if done:
            last_color, last_val = self.what_has_been_clicked[-1]
            emoji = EMOJI_MAP[last_color]
            lines[-1] = f"{emoji} **+{last_val}** (Stock: **{self.current_score}**)"

        return "\n".join(lines)

    def callback2(self, index: int):
        async def button_callback(interaction: discord.Interaction):
            if not self.game_active:
                return await interaction.response.send_message("game is over!", ephemeral=True)

            cell = self.grid_data[index]
            if cell["revealed"]:
                return await interaction.response.send_message("should not be clickable blud.")

            cell["revealed"] = True
            color = cell["color"]
            value = cell["value"]

            self.current_score += value
            self.clicks_remaining -= 1
            self.what_has_been_clicked.append((color, value))

            for child in self.children:
                if child.custom_id == f"oc_{index}":
                    child.emoji = EMOJI_MAP[color]
                    child.style = discord.ButtonStyle.blurple
                    child.disabled = True
                    break

            status_text = (
                "You can click **5** times on the buttons below (2 minutes).\n"
                "**1 red sphere** to find (never at the center) along with **2 orange** (always next to the red sphere), "
                "**3 yellow** (always diagonal to the red sphere), **4 green** (in the same row or column as red), "
                "**teal** (in the same row, column or diagonal as red) and **blue** (NEVER in the same row, column nor diagonal from red).\n​"
            )

            if self.clicks_remaining == 0:
                self.game_active = False
                for i, child in enumerate(self.children):
                    child.disabled = True
                    if not self.grid_data[i]["revealed"]:
                        rem_color = self.grid_data[i]["color"]
                        child.emoji = EMOJI_MAP[rem_color]
                        child.style = discord.ButtonStyle.secondary

            await interaction.response.edit_message(content=status_text, view=self)
            is_finished = (self.clicks_remaining == 0)
            log_text = self.i_have_a_big_log(done=is_finished)

            if self.log_message is None:
                self.log_message = await interaction.channel.send(log_text)
                return None
            else:
                await self.log_message.edit(content=log_text)
                return None

        return button_callback