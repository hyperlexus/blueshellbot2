import json
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
            await interaction.followup.send("premoved your command again, hast du's jetzt bald?", ephemeral=True)
        else:
            await interaction.response.send_message("error removing command, it might have been removed already", ephemeral=True)


class PizzaSingleResultView(discord.ui.View):
    def __init__(self, command_dict, bot, data_ref, embeds_ref, author_ref):
        super().__init__(timeout=60)
        self.command = command_dict
        self.bot = bot
        self.data_ref = data_ref
        self.author_ref = author_ref
        self.__embeds = embeds_ref

    @discord.ui.button(label="info", style=discord.ButtonStyle.primary, emoji="💡")
    async def info_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if str(interaction.user.id) != self.author_ref:
            return await interaction.response.send_message("This offer doesn't match any of yours")
        author_name = str(self.bot.get_user(int(self.command['author']))).split(' ')[0]
        real_time = int(self.command['time']) // 1000
        embed = self.__embeds.SLASH_PINFO_PREMOVE_RESULT(
            real_time, author_name, self.command['read'], self.command['write'], mode="info"
        )
        await interaction.response.send_message(embed=embed)

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
        await interaction.followup.send(f"command `{command_id}` has been removed.")
