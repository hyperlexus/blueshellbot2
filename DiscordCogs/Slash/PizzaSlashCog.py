import json
import math
import random
from collections import deque
import discord
from pizza_eval import pizza_eval_write, pizza_eval_read, errors
from Music.BlueshellBot import BlueshellBot
from discord import ApplicationContext, Option, OptionChoice
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from UI.PizzaViews import PizzaUndoView, PizzaSingleResultView, PizzaConsentView, PizzaPaginationView
from Utils.BoolDiscordFormatting import evaluate_discord_timestamp
from Utils.Utils import Utils

helper = Helper()

with open("database.json", "r") as f:
    data = json.load(f)

try:
    with open("Storage/pizza_lb.json", "r") as f_lb:
        pizza_lb = json.load(f_lb)
except (FileNotFoundError, json.JSONDecodeError):
    pizza_lb = {}

pizza_tiers = {
    1000: "<:pizza_champion:1520095859159732334>",
    640: "<:pizza_grandmaster:1520095823235645480>",
    320: "<:pizza_master:1520095781229432945>",
    160: "<:pizza_diamond:1520095746970615818>",
    80: "<:pizza_platinum:1520095709968335109>",
    40: "<:pizza_gold:1520095667299680546>",
    20: "<:pizza_silver:1520095621556605060>",
    10: "<:pizza_bronze:1520095589247877200>"
}


class PizzaSlashCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.is_muted = False
        self.last_10_messages = deque(maxlen=10)

    @Cog.listener()
    async def on_message(self, message):
        if self.__bot.voice_clients:
            return None
        if message.author.id == 1509153361000136825:
            return await message.add_reaction("🤫")
        if self.is_muted or message.author == self.__bot.user or not message.content:
            return None
        if "nopizza" in (str(message.channel.topic) if isinstance(message.channel, discord.TextChannel) else ""):
            return None

        pizza_messages = []
        is_a_dm = message.guild is None
        has_pizza_role = any(role.id == self.__config.PIZZA_ROLE for role in message.author.roles) if message.author.roles is not None else False
        is_okay_server = (not is_a_dm and message.guild.id == self.__config.PIZZA_SERVER and has_pizza_role)
        if not (is_a_dm or is_okay_server):
            return None
        for current_dict in data['p_commands']:
            try:
                if not pizza_eval_read(current_dict['read'], message.content):
                    continue
                if "[replace\\" in current_dict['write'] and len(message.content) > 50:
                    continue
                evaluated_msg = pizza_eval_write(str(message.author).split(" ")[0], message.content, current_dict['write'])
                pizza_messages.append((current_dict['time'], evaluated_msg))
            except errors.PizzaError as e:
                ctx = await self.__bot.get_context(message)
                details = e.args[0]
                await ctx.send(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))

        if not pizza_messages:
            return None

        # 過去10件にないメッセージを選んで送ってください。#2
        possible = [m for m in pizza_messages if m[1] not in self.last_10_messages]
        if not possible:
            return None

        chosen_command_id, to_send = random.choice(possible)
        self.last_10_messages.append(to_send)
        content = to_send if to_send else "\u2800"

        if chosen_command_id not in pizza_lb:
            pizza_lb[chosen_command_id] = 0
        pizza_lb[chosen_command_id] += 1

        with open("Storage/pizza_lb.json", "w") as f_lb:
            json.dump(pizza_lb, f_lb, indent=4)

        count = pizza_lb[chosen_command_id]
        emoji_to_append = ""

        for threshold, emoji in pizza_tiers.items():
            if count == threshold:
                emoji_to_append = emoji
        if emoji_to_append:
            content = f"{emoji_to_append} {content}"
        return await message.channel.send(content)

    @slash_command(name="pinsert", description=helper.HELP_PINSERT)
    async def pinsert(self, ctx: ApplicationContext,
                      read = Option(str, "The string to match. The compiler works on this one"),
                      write = Option(str, "What pizza romani responds with. The [] syntax goes here")):
        if not self.__bot.listingSlash: return None
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            return await ctx.respond(embed=self.__embeds.BANNED())
        await ctx.defer()

        # initialise all variables that will be passed to the json
        time = str((ctx.interaction.id >> 22) + 1420070400000)
        author = str(ctx.interaction.user.id)
        author_name = self.__bot.get_user(author)

        try:
            pizza_eval_read(read, 'soos')
            pizza_eval_write(author_name, 'siis', write)
        except errors.PizzaError as e:
            details = e.args[0]
            return await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))

        if '@everyone' in write or '@here' in write:
            return await ctx.send("please do not attempt to make pizza ping everyone!")

        new_command = {
            "time": time,
            "author": author,
            "read": read,
            "write": write
        }

        data['p_commands'].append(new_command)

        with open("database.json", "w") as f2:
            json.dump(data, f2, indent=4)

        view = PizzaUndoView(
            command_id=time,
            data_ref=data,
            author_ref=author,
            config_path=self.__config.PROJECT_PATH,
            embeds_ref=self.__embeds
        )

        return await ctx.respond(embed=self.__embeds.PIZZA_INSERTED(read, write, time), view=view)

    @slash_command(name="pedit", description=helper.HELP_PEDIT)
    async def pedit(self, ctx: ApplicationContext,
                    command_id: Option = Option(int, description="command id. you can get this from /plist"),
                    filter_category: Option = Option(str, choices=[
                        OptionChoice(name='read', value='read'),
                        OptionChoice(name='write', value='write')]),
                    new_input: Option = Option(str, description="what to replace the current content with")
                    ):
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            return await ctx.respond(embed=self.__embeds.BANNED())
        await ctx.defer()

        valid_command = None
        for current_dict in data['p_commands']:
            if current_dict['time'] == str(command_id):
                valid_command = current_dict
                break

        if valid_command is None:
            return await ctx.respond(embed=self.__embeds.SLASH_PIZZA_NOTHING_FOUND(command_id))

        try:
            if filter_category == 'read':
                pizza_eval_read(new_input, 'soos')
            else:  # write
                author_name = str(ctx.interaction.user).split(" ")[0]
                pizza_eval_write(author_name, 'siis', new_input)
        except errors.PizzaError as e:
            details = e.args[0]
            return await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))

        if filter_category == 'write' and ('@everyone' in new_input or '@here' in new_input):
            return await ctx.send("please do not attempt to make pizza ping everyone!")

        original_author_id = valid_command['author']
        is_original_author = str(ctx.interaction.user.id) == original_author_id

        if is_original_author or original_author_id == "0":
            valid_command[filter_category] = new_input
            with open("database.json", "w") as f2:
                json.dump(data, f2, indent=4)
            return await ctx.respond(f"edited `{filter_category}` value for command `{command_id}`!")
        else:
            old_input = valid_command[filter_category]
            view = PizzaConsentView(
                original_author_id=original_author_id,
                data_ref=data,
                command_id=str(command_id),
                filter_category=filter_category,
                new_input=new_input
            )

            prompt_message = (
                f"<@{original_author_id}>, {ctx.interaction.user.display_name} wants to change the "
                f"`{filter_category}` category of your pizza command `{command_id}` from\n```\n{old_input}\n```\nto:\n```\n{new_input}\n```\n"
                f"Do you consent?"
            )
            return await ctx.respond(prompt_message, view=view)

    @slash_command(name="plist", description=helper.HELP_PLIST)
    async def plist(self, ctx: ApplicationContext,
                    filter_category = Option(str, choices=[
                        OptionChoice(name='time', value='time'),
                        OptionChoice(name='author', value='author'),
                        OptionChoice(name='read', value='read'),
                        OptionChoice(name='write', value='write')],
                                            description="What type to filter by. Requires string_to_match to be passed as well.",
                                            default=None),
                    string_to_match: Option = Option(str,
                                            description="String to filter by. Requires command_filter to be passed as well.", default=None),
                    page: Option = Option(int,
                                 "which page of list to show. may be required if output is longer than 25 lines", default=None)
                    ):
        if not self.__bot.listingSlash: return None
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            return await ctx.respond(embed=self.__embeds.BANNED())

        if bool(filter_category) ^ bool(string_to_match):  # first ever use of xor recorded in humanity
            return await ctx.respond(embed=self.__embeds.SLASH_PLIST_NOT_BOTH_OPTIONS())
        await ctx.defer()

        current_page = (page - 1) if page and page > 0 else 0

        if filter_category == "author":
            raw_match = string_to_match
            string_to_match = str(Utils.ping_to_id(string_to_match))
            if string_to_match == 'False':  # なんでこうなってるのか謎だし微妙だなって思ってますが、いじるのはやめておきますね
                return await ctx.respond(embed=self.__embeds.BAD_USER_ID(raw_match))

        if not filter_category:
            filtered = data['p_commands']
        elif filter_category == "time":
            filtered = [d for d in data['p_commands'] if evaluate_discord_timestamp(int(d['time']) // 1000, string_to_match)]
        else:
            filtered = [d for d in data['p_commands'] if string_to_match.lower() in d.get(filter_category, "").lower()]

        total_amount = len(filtered)
        if total_amount == 0:
            return await ctx.respond(embed=self.__embeds.PIZZA_LIST("No commands found."))

        command_list = []
        count, ranked = 0, ""
        for d in filtered:
            cmd_id = str(d['time'])
            count = pizza_lb.get(cmd_id, 0)
            current_rank_emoji = ""

            for threshold, emoji in pizza_tiers.items():
                if count >= threshold:
                    current_rank_emoji = f" {emoji}"
                    break

            ranked = f"{current_rank_emoji} "

            if len(d['write']) > 2000 or len(d['read']) > 2000:
                command_list.append(f"{ranked}{cmd_id}: command too long to display.")
            else:
                command_list.append(f"{ranked}{cmd_id}: {d['read']} -> {d['write']}")

        if total_amount == 1:
            view = PizzaSingleResultView(
                command_dict=filtered[0], bot=self.__bot, data_ref=data,
                embeds_ref=self.__embeds, author_ref=str(ctx.interaction.user.id),
                uses_ref=count, rank_emoji_ref=ranked
            )
            embed = (self.__embeds.PIZZA_LIST_FILTERED(command_list[0], filter_category, string_to_match)
                     if filter_category else self.__embeds.PIZZA_LIST(command_list[0]))
            return await ctx.respond(embed=embed, view=view)

        def generate_plist_embed(result_text, curr_page, tot_pages):
            if len(result_text) > 4096:
                longest = max(result_text.splitlines(), key=len)
                result_text = f"command list was too long. length was {len(result_text)}.\nlongest command (first 1k characters):\n{longest[:1000]}"

            list_embed = (self.__embeds.PIZZA_LIST_FILTERED(result_text, filter_category, string_to_match)
                     if filter_category else self.__embeds.PIZZA_LIST(result_text))
            if tot_pages > 1:
                list_embed.set_footer(text=f"page {curr_page}/{tot_pages}")
            return list_embed

        current_page_idx = (page - 1) if page and page > 0 else 0
        view = PizzaPaginationView(
            items=command_list,
            embed_generator=generate_plist_embed,
            per_page=25,
            starting_page=current_page_idx
        )

        return await ctx.respond(embed=view.get_current_embed(), view=view)

    @slash_command(name="pinfo", description=helper.HELP_PINFO)
    async def pinfo(self, ctx: ApplicationContext,
                    command_id = Option(int, "Command id. You can get this from /plist")):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        valid_command = None
        for current_dict in data['p_commands']:
            if current_dict['time'] == str(command_id):
                if valid_command is None:
                    valid_command = current_dict
                else:
                    await ctx.respond(embed=self.__embeds.SLASH_PIZZA_MORE_THAN_ONE_COMMAND_WITH_SAME_ID(command_id))
                    return

        if valid_command is None:
            await ctx.respond(embed=self.__embeds.SLASH_PIZZA_NOTHING_FOUND(command_id))
            return
        else:
            author_name = str(self.__bot.get_user(int(valid_command['author']))).split(' ')[0]
            real_time = int(valid_command['time']) // 1000
            count = pizza_lb.get(str(command_id), 0)
            current_rank_emoji = ""

            for threshold, emoji in pizza_tiers.items():
                if count >= threshold:
                    current_rank_emoji = emoji
                    break

            await ctx.respond(
                embed=self.__embeds.SLASH_PINFO_PREMOVE_RESULT(
                    real_time, author_name, valid_command['read'], valid_command['write'], mode="info",
                    uses=count, rank_emoji=current_rank_emoji
                )
            )

    # noinspection DuplicatedCode
    @slash_command(name="premove", description=helper.HELP_PREMOVE)
    async def premove(self, ctx: ApplicationContext,
                      command_id = Option(int, "Command id. You can get this from /plist")):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        valid_command = None
        for current_dict in data['p_commands']:
            if current_dict['time'] == str(command_id):
                if valid_command is None:
                    valid_command = current_dict
                else:
                    await ctx.respond(embed=self.__embeds.SLASH_PIZZA_MORE_THAN_ONE_COMMAND_WITH_SAME_ID(command_id))
                    return

        if valid_command is None:
            await ctx.respond(embed=self.__embeds.SLASH_PIZZA_NOTHING_FOUND(command_id))
            return
        else:
            author_name = str(self.__bot.get_user(int(valid_command['author']))).split(' ')[0]
            real_time = int(valid_command['time']) // 1000
            await ctx.respond(embed=self.__embeds.SLASH_PINFO_PREMOVE_RESULT(
                real_time, author_name, valid_command['read'], valid_command['write'], mode="remove"))
            data['p_commands'] = [d for d in data['p_commands'] if d != valid_command]

            if str(command_id) in pizza_lb:
                del pizza_lb[str(command_id)]
                with open("pizza_lb.json", "w") as f_lb:
                    json.dump(pizza_lb, f_lb, indent=4)

        with open("database.json", "w") as f2:
            json.dump(data, f2, indent=4)
        return

    @slash_command(name="ptestcompiler", description=helper.HELP_COMPILER)
    async def ptestcompiler(self, ctx: ApplicationContext,
                            read = Option(str, "The string to match. The compiler works on this one"),
                            write = Option(str, "What pizza romani responds with. The [] syntax goes here"),
                            message = Option(str, "test message")):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        try:
            if not pizza_eval_read(read, message):
                await ctx.respond("read check didn't pass.")
                return
            write = pizza_eval_write(str(ctx.interaction.user)[:-2], message, write)
        except errors.PizzaError as e:
            details = e.args[0]
            await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return

        await ctx.respond(write)

    @slash_command(name="pmute", description=helper.HELP_PMUTE)
    async def pmute(self, ctx: ApplicationContext):
        bot_admins = self.__config.BOT_ADMINS.split(",")
        if str(ctx.interaction.user.id) not in bot_admins:
            await ctx.respond("You must be a bot admin to mute/unmute pizza romani!")
            return
        self.is_muted = not self.is_muted
        if self.is_muted:
            await ctx.respond("Pizza Romani has been muted. :( Please unmute him soon or he will be sad.")
        else:
            await ctx.respond("Hooray, Pizza Romani is able to participate in conversation again! Yippie.")

    @slash_command(name="phelp", description=helper.HELP_PHELP)
    async def phelp(self, ctx: ApplicationContext,
                    command = Option(str, choices=[
                        OptionChoice(name='pinsert', value='pinsert'),
                        OptionChoice(name='plist', value='plist'),
                        OptionChoice(name='pinfo', value='pinfo'),
                        OptionChoice(name='premove', value='premove'),
                        OptionChoice(name='ptestcompiler', value='compiler')])):
        output = f"# {command} help"
        await ctx.interaction.response.defer()
        match command:
            case "plist":
                output = helper.HELP_PLIST_LONG
            case "pinfo":
                output = helper.HELP_PINFO_LONG
            case "premove":
                output = helper.HELP_PREMOVE_LONG
            case "compiler":
                output = helper.HELP_COMPILER_LONG
            case "pinsert":
                with open("Utils/PizzaEval/pizza_help_read") as f3:
                    output = f3.read()
                with open("Utils/PizzaEval/pizza_help_write") as f4:
                    output_write = f4.read()
        await ctx.interaction.followup.send(output)
        if command == "pinsert":
            await ctx.interaction.followup.send(output_write)

    @slash_command(name="ptop", description="Displays a ranking of the top most used pizza commands.")
    async def ptop(self, ctx: ApplicationContext,
                   page: Option = Option(int, "which page to show.", default=None)):
        if not self.__bot.listingSlash:
            return None
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            return await ctx.respond(embed=self.__embeds.BANNED())
        await ctx.defer()

        if not pizza_lb:
            empty_embed = discord.Embed(
                title="Pizza Leaderboard empty",
                description="maybe wrong database location?",
                color=self.__colors.BLUE
            )
            return await ctx.respond(embed=empty_embed)

        sorted_lb = sorted(pizza_lb.items(), key=lambda item: item[1], reverse=True)

        description_lines = []
        for index, (cmd_id, count) in enumerate(sorted_lb):
            current_rank_emoji = ""
            for threshold, emoji in pizza_tiers.items():
                if count >= threshold:
                    current_rank_emoji = f" {emoji}"
                    break
            cmd_details = next((d for d in data['p_commands'] if d['time'] == cmd_id), None)

            if cmd_details:
                read_val = cmd_details['read'][:25] + ("..." if len(cmd_details['read']) > 25 else "")
                write_val = cmd_details['write'][:35] + ("..." if len(cmd_details['write']) > 35 else "")
                line = f"\\#{index + 1}: {current_rank_emoji} {count} | {read_val} ➔ {write_val}"
            else:
                line = f"\\#{index + 1}: {current_rank_emoji} {count} | command was removed."

            description_lines.append(line)

        def generate_ptop_embed(result_text, curr_page, tot_pages):
            embed = discord.Embed(
                title="Pizza command leaderboard",
                description=result_text,
                color=self.__colors.BLUE
            )
            if tot_pages > 1:
                embed.set_footer(text=f"Page {curr_page} of {tot_pages}")
            return embed

        current_page_idx = (page - 1) if page and page > 0 else 0
        view = PizzaPaginationView(
            items=description_lines,
            embed_generator=generate_ptop_embed,
            per_page=10,
            starting_page=current_page_idx
        )

        return await ctx.respond(embed=view.get_current_embed(), view=view)


def setup(bot):
    bot.add_cog(PizzaSlashCog(bot))