import json
import math
import random
from collections import deque

import discord

from Music.BlueshellBot import BlueshellBot
from discord import ApplicationContext, Option, OptionChoice
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from UI.PizzaViews import PizzaUndoView, PizzaSingleResultView
from Utils.PizzaEval import PizzaEvalErrorDict, PizzaEvalUtils
from Utils.PizzaEval.PizzaEvaluator import pizza_eval_read
from Utils.PizzaEval.PizzaEvaluatorWrite import pizza_eval_write
from Utils.BoolDiscordFormatting import evaluate_discord_timestamp
from Utils.Utils import Utils

helper = Helper()

with open("database.json", "r") as f:
    data = json.load(f)


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
            return
        if self.is_muted or message.author == self.__bot.user or not message.content:
            return
        if "nopizza" in (str(message.channel.topic) if isinstance(message.channel, discord.TextChannel) else ""):
            return

        pizza_messages = []
        is_a_dm = message.guild is None
        is_okay_server = (not is_a_dm and message.guild.id == self.__config.PIZZA_SERVER and any(role.id == self.__config.PIZZA_ROLE for role in message.author.roles))
        if not (is_a_dm or is_okay_server):
            return
        for current_dict in data['p_commands']:
            try:
                if not pizza_eval_read(current_dict['read'], message.content):
                    continue

                if "[replace\\" in current_dict['write'] and len(message.content) > 50:
                    continue
                pizza_messages.append(pizza_eval_write(str(message.author).split(" ")[0], message.content, current_dict['write']))
            except PizzaEvalUtils.PizzaError as e:
                ctx = await self.__bot.get_context(message)
                details = e.args[0]
                await ctx.send(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))

        if not pizza_messages:
            return

        # 過去10件にないメッセージを選んで送ってください。
        possible = [m for m in pizza_messages if m not in self.last_10_messages]
        if not possible:
            return
        to_send = random.choice(possible)
        self.last_10_messages.append(to_send)
        content = to_send if to_send else "\u2800"
        await message.channel.send(content)
        return

    @slash_command(name="pinsert", description=helper.HELP_PINSERT)
    async def pinsert(self, ctx: ApplicationContext,
                      read: Option(str, "The string to match. The compiler works on this one"),
                      write: Option(str, "What pizza romani responds with. The [] syntax goes here")):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        # initialise all variables that will be passed to the json
        time = str((ctx.interaction.id >> 22) + 1420070400000)
        author = str(ctx.interaction.user.id)
        author_name = self.__bot.get_user(author)

        try:
            PizzaEvalErrorDict.recursion_counter = 0
            pizza_eval_read(read, 'soos')
            pizza_eval_write(author_name, 'siis', write)
        except PizzaEvalUtils.PizzaError as e:
            details = e.args[0]
            await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return

        if '@everyone' in write or '@here' in write:
            await ctx.send("please do not attempt to make pizza ping everyone!")
            return

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

        await ctx.respond(embed=self.__embeds.PIZZA_INSERTED(read, write, time),
                          view=view)
        return

    @slash_command(name="plist", description=helper.HELP_PLIST)
    async def plist(self, ctx: ApplicationContext,
                    filter_category: Option(str, choices=[
                        OptionChoice(name='time', value='time'),
                        OptionChoice(name='author', value='author'),
                        OptionChoice(name='read', value='read'),
                        OptionChoice(name='write', value='write')],
                                            description="What type to filter by. Requires string_to_match to be passed as well.") = None,
                    string_to_match: Option(str,
                                            "String to filter by. Requires command_filter to be passed as well.") = None,
                    page: Option(int,
                                 "which page of list to show. may be required if output is longer than 25 lines") = None
                    ):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()
        author = str(ctx.interaction.user.id)

        if bool(filter_category) ^ bool(string_to_match):  # first ever use of xor recorded in humanity
            await ctx.respond(embed=self.__embeds.SLASH_PLIST_NOT_BOTH_OPTIONS())

        command_list = []
        button_list = []
        if page:
            page = page - 1 if page > 0 else 1

        if filter_category == "author":
            tempstring_if_conversion_doesnt_work = string_to_match
            string_to_match = str(Utils.ping_to_id(string_to_match))
            if string_to_match == 'False':
                await ctx.respond(embed=self.__embeds.BAD_USER_ID(tempstring_if_conversion_doesnt_work))
                return

        for current_dict in data['p_commands']:
            add_command = False
            if not filter_category:
                add_command = True
            else:
                if filter_category == "time":
                    if evaluate_discord_timestamp(int(current_dict['time']) // 1000, string_to_match):
                        add_command = True
                elif string_to_match in current_dict[filter_category]:
                    add_command = True
            if add_command:
                button_list.append(current_dict)
                if len(current_dict['write']) > 2000 or len(current_dict['read']) > 2000:
                    command_list.append(
                        f"{current_dict['time']}: this command is longer than 2k characters, so it won't be included. it's probably the wahlkommission command.")
                else:
                    command_list.append(f"{current_dict['time']}: {current_dict['read']} -> {current_dict['write']}")

        amount_pages = math.ceil(len(command_list) / 25)

        if len(command_list) == 0:
            result = "No commands found."
        else:
            if len(command_list) > 25:
                if page is None:
                    await ctx.respond(embed=self.__embeds.PIZZA_LIST_TOO_LONG(len(command_list), amount_pages))
                    return
                else:
                    if page >= math.ceil(len(command_list) / 25):
                        await ctx.respond(
                            embed=self.__embeds.SLASH_PLIST_PAGE_LARGER_THAN_AMOUNT_COMMANDS(amount_pages))
                        return
                    command_list = command_list[page * 25:page * 25 + 25]
            result = "\n".join(command_list)
            if len(result) > 4096:
                longest = ""
                for i in result.split("\n"):
                    longest = i if len(i) > len(longest) else longest
                result = f"command list was too long. length was {len(result)}.\nlongest command (first 1k characters):\n{longest[:1000]}"

        view = None
        if len(button_list) == 1:
            view = PizzaSingleResultView(
                command_dict=button_list[0],
                bot=self.__bot,
                data_ref=data,
                embeds_ref=self.__embeds,
                author_ref=author
            )

        if not filter_category:
            await ctx.respond(embed=self.__embeds.PIZZA_LIST(result), view=view)
        else:
            await ctx.respond(embed=self.__embeds.PIZZA_LIST_FILTERED(result, filter_category, string_to_match), view=view)
        return

    @slash_command(name="pinfo", description=helper.HELP_PINFO)
    async def pinfo(self, ctx: ApplicationContext,
                    command_id: Option(int, "Command id. You can get this from /plist")):
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
                real_time, author_name, valid_command['read'], valid_command['write'], mode="info"))
            return

    # noinspection DuplicatedCode
    @slash_command(name="premove", description=helper.HELP_PREMOVE)
    async def premove(self, ctx: ApplicationContext,
                      command_id: Option(int, "Command id. You can get this from /plist")):
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

        with open("database.json", "w") as f2:
            json.dump(data, f2, indent=4)
        return

    @slash_command(name="ptestcompiler", description=helper.HELP_COMPILER)
    async def ptestcompiler(self, ctx: ApplicationContext,
                            read: Option(str, "The string to match. The compiler works on this one"),
                            write: Option(str, "What pizza romani responds with. The [] syntax goes here"),
                            message: Option(str, "test message")):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        try:
            PizzaEvalErrorDict.recursion_counter = 0
            if not pizza_eval_read(read, message):
                await ctx.respond("read check didn't pass.")
                return
            write = pizza_eval_write(str(ctx.interaction.user)[:-2], message, write)
        except PizzaEvalUtils.PizzaError as e:
            details = e.args[0]
            await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return

        await ctx.respond(write)

    @slash_command(name="pmute", description=helper.HELP_PMUTE)
    async def pmute(self, ctx: ApplicationContext):
        bot_admins = self.__config.BOT_ADMINS.split(",")
        print(bot_admins, ctx.interaction.user.id)
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
                    command: Option(str, choices=[
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


def setup(bot):
    bot.add_cog(PizzaSlashCog(bot))
