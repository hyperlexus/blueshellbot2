import json
import math
from datetime import datetime, timezone

from Music.BlueshellBot import BlueshellBot
from discord import ApplicationContext, Option, OptionChoice, Enum
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.PizzaEval import PizzaEvalErrorDict, PizzaEvalUtils
from Utils.PizzaEval.PizzaEvalUtils import logical_xor
from Utils.PizzaEval.PizzaEvaluator import pizza_eval_read
from Utils.Utils import Utils

helper = Helper()

with open("pizza_database.json", "r") as f:
    data = json.load(f)

class PizzaSlashCog(Cog):
    """
    Class to listen to Music commands
    It'll listen for commands from discord, when triggered will create a specific Handler for the command
    Execute the handler and then create a specific View to be showed in Discord
    """

    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.__bot.user or message.content.lower().startswith('b.p') or not message.content:
            return
        ctx = await self.__bot.get_context(message)

        for current_dict in data['p_commands']:
            send = False

            try:
                send = pizza_eval_read(current_dict['read'], message.content.lower())
            except PizzaEvalUtils.PizzaError as e:
                details = e.args[0]
                await ctx.send(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))

            if send and (message.guild is None or message.guild.id != self.__config.PIZZA_SERVER or any(
                    role.id == self.__config.PIZZA_ROLE for role in message.author.roles)):
                if current_dict['write'].startswith('b.'):  # make it be able to eval its own commands :)
                    command_and_args = current_dict['write'][2:].split(" ")
                    command_to_run = self.__bot.get_command(command_and_args[0])
                    await ctx.invoke(command_to_run, *command_and_args[1:])
                    continue
                await message.channel.send(current_dict['write'])

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

        try:
            PizzaEvalErrorDict.recursion_counter = 0
            pizza_eval_read(read, 'a')
        except PizzaEvalUtils.PizzaError as e:
            details = e.args[0]
            await ctx.respond(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return

        new_command = {
            "time": time,
            "author": author,
            "read": read,
            "write": write
        }

        data['p_commands'].append(new_command)

        with open("pizza_database.json", "w") as f2:
            json.dump(data, f2, indent=4)

        await ctx.respond(embed=self.__embeds.PIZZA_INSERTED(read, write))
        return

    @slash_command(name="plist", description=helper.HELP_PLIST)
    async def plist(self, ctx: ApplicationContext,
                    filter_category: Option(str, choices=[
                        OptionChoice(name='time', value='time'),
                        OptionChoice(name='author', value='author'),
                        OptionChoice(name='read', value='read'),
                        OptionChoice(name='write', value='write')],
                        description="What type to filter by. Requires string_to_match to be passed as well.") = None,
                    string_to_match: Option(str, "String to filter by. Requires command_filter to be passed as well.") = None,
                    page: Option(int, "which page of list to show. may be required if output is longer than 25 lines") = None
                    ):
        if not self.__bot.listingSlash:
            return
        if Utils.check_if_banned(ctx.interaction.user.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer()

        if bool(filter_category) ^ bool(string_to_match):  # first ever use of xor recorded in humanity
            await ctx.respond(embed=self.__embeds.SLASH_PLIST_NOT_BOTH_OPTIONS())

        command_list = []
        if page:
            page = page - 1 if page > 0 else 1

        if filter_category == "author":
            tempstring_if_conversion_doesnt_work = string_to_match
            string_to_match = str(Utils.ping_to_id(string_to_match))
            if string_to_match == 'False':
                await ctx.respond(embed=self.__embeds.BAD_USER_ID(tempstring_if_conversion_doesnt_work))
                return

        for index, current_dict in enumerate(data['p_commands']):
            if not filter_category:
                command_list.append({current_dict['read']: current_dict['write']})
            else:
                if not filter_category == "time":
                    if string_to_match in current_dict[filter_category]:
                        command_list.append({current_dict['read']: current_dict['write']})
                else:
                    if Utils.bool_discord_time_syntax('a', 'b'):
                        pass  # LEFT OFF HERE, THIS IS TO DO NEXT


        amount_pages = math.ceil(len(command_list) / 25) - 1

        if len(command_list) == 0:
            result = "No commands found."
        else:
            if len(command_list) > 25:
                if page is None:
                    await ctx.respond(embed=self.__embeds.PIZZA_LIST_TOO_LONG(len(command_list), amount_pages))
                    return
                else:
                    if page >= math.ceil(len(command_list) / 25):
                        print("nigger")
                    command_list = command_list[page*25:page*25+25]
            result = "\n".join(f"{key} -> {value}" for adict in command_list for key, value in adict.items())

        if not filter_category:
            await ctx.respond(embed=self.__embeds.PIZZA_LIST(result))
        else:
            await ctx.respond(embed=self.__embeds.PIZZA_LIST_FILTERED(result, filter_category, string_to_match))
        return

def setup(bot):
    bot.add_cog(PizzaSlashCog(bot))
