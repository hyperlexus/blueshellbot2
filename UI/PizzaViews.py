import json
import math

import discord

class PizzaUndoView(discord.ui.View):
    def __init__(self, command_id, data_ref, config_path, embeds_ref, author_ref):
        super().__init__(timeout=60)
        self.command_id = str(command_id)
        self.data_ref = data_ref
        self.author_ref = author_ref
        self.config_path = config_path
        self.__embeds = embeds_ref

    @discord.ui.button(label="Undo", style=discord.ButtonStyle.danger, emoji="💣")
    async def undo_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.author_ref:
            return await interaction.response.send_message("This offer doesn't match any of yours")
        original_len = len(self.data_ref['p_commands'])
        self.data_ref['p_commands'] = [d for d in self.data_ref['p_commands'] if d['time'] != self.command_id]

        if len(self.data_ref['p_commands']) < original_len:
            # update
            with open("database.json", "w") as f:
                json.dump(self.data_ref, f, indent=4)

            button.disabled = True
            button.label = "nevermind"
            await interaction.response.edit_message(view=self)
            return await interaction.followup.send("premoved your command again, hast du's jetzt bald?")
        else:
            return await interaction.response.send_message("error removing command, it might have been removed already")


class PizzaSingleResultView(discord.ui.View):
    def __init__(self, command_dict, bot, data_ref, embeds_ref, author_ref, uses_ref = 0, rank_emoji_ref = ""):
        super().__init__(timeout=60)
        self.command = command_dict
        self.bot = bot
        self.data_ref = data_ref
        self.author_ref = author_ref
        self.__embeds = embeds_ref
        self.uses_ref = uses_ref
        self.rank_emoji_ref = rank_emoji_ref

    @discord.ui.button(label="info", style=discord.ButtonStyle.primary, emoji="💡")
    async def info_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.author_ref:
            return await interaction.response.send_message("This offer doesn't match any of yours")
        author_name = str(self.bot.get_user(int(self.command['author']))).split(' ')[0]
        real_time = int(self.command['time']) // 1000
        embed = self.__embeds.SLASH_PINFO_PREMOVE_RESULT(
            real_time, author_name, self.command['read'], self.command['write'], mode="info",
            uses=self.uses_ref, rank_emoji=self.rank_emoji_ref
        )
        return await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="remove", style=discord.ButtonStyle.danger, emoji="💣")
    async def remove_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.author_ref:
            return await interaction.response.send_message("This offer doesn't match any of yours")
        command_id = self.command['time']
        self.data_ref['p_commands'] = [d for d in self.data_ref['p_commands'] if d['time'] != command_id]

        with open("database.json", "w") as f:
            json.dump(self.data_ref, f, indent=4)

        for item in self.children:
            item.disabled = True
            if button.label == "remove":
                button.label = "removed."

        await interaction.response.edit_message(view=self)
        return await interaction.followup.send(f"command `{command_id}` has been removed.")

class PizzaConsentView(discord.ui.View):
    def __init__(self, original_author_id: str, data_ref: dict, command_id: str, filter_category: str, new_input: str):
        super().__init__(timeout=300)
        self.original_author_id = original_author_id
        self.data_ref = data_ref
        self.command_id = command_id
        self.filter_category = filter_category
        self.new_input = new_input

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, emoji="<:kekmark:1506816979804229752>")
    async def confirm(self, _button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.original_author_id:
            return await interaction.response.send_message("you may not give consent for someone else.")

        target = next((d for d in self.data_ref['p_commands'] if d['time'] == self.command_id), None)
        if target:
            target[self.filter_category] = self.new_input
            with open("database.json", "w") as f:
                json.dump(self.data_ref, f, indent=4)
            return await interaction.response.edit_message(content=f"you have consented to the command `{self.command_id}` being updated.", view=None)
        else:
            return await interaction.response.edit_message(content="some error occurred while trying to consent.", view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger, emoji="❌")
    async def cancel(self, _button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.original_author_id:
            return await interaction.response.send_message("you may not deny consent for someone else.")
        return await interaction.response.edit_message(content=f"you have not given consent. remember, no means no!", view=None)


class PizzaPaginationView(discord.ui.View):
    def __init__(self, items: list[str], embed_generator, per_page: int = 25, starting_page: int = 0):
        super().__init__(timeout=300)
        self.items = items
        self.embed_generator = embed_generator
        self.per_page = per_page
        self.total_pages = math.ceil(len(items) / per_page) or 1
        self.current_page = max(0, min(starting_page, self.total_pages - 1))

        if self.total_pages <= 1:  # if result amount < 26, remove buttons since only 1 page
            self.remove_item(self.prev_button)
            self.remove_item(self.next_button)

    def get_current_embed(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_items = self.items[start:end]
        result_string = "\n".join(page_items) if page_items else "No items found."
        return self.embed_generator(result_string, self.current_page + 1, self.total_pages)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary, custom_id="prev")
    async def prev_button(self, _button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = (self.current_page-1) % self.total_pages  # ich bin genial
        return await interaction.response.edit_message(embed=self.get_current_embed(), view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary, custom_id="next")
    async def next_button(self, _button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = (self.current_page + 1) % self.total_pages
        return await interaction.response.edit_message(embed=self.get_current_embed(), view=self)
