import asyncio
import json
from copy import deepcopy
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.PizzaEval.PizzaEvaluator import pizza_eval_read
from Utils.PizzaEval import PizzaEvalErrorDict, PizzaEvalUtils
from Utils.Utils import Utils
helper = Helper()
PizzaEvalErrorDict.recursion_counter = 0

with open("pizza_database.json", "r") as f:
    data = json.load(f)

# noinspection DuplicatedCode
class PizzaRomaniCog(Cog):
    """ich ess pizza"""
    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

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

            if send and (message.guild is None or message.guild.id != self.__config.PIZZA_SERVER or any(role.id == self.__config.PIZZA_ROLE for role in message.author.roles)):
                if current_dict['write'].startswith('b.'):  # make it be able to eval its own commands :)
                    command_and_args = current_dict['write'][2:].split(" ")
                    command_to_run = self.__bot.get_command(command_and_args[0])
                    await ctx.invoke(command_to_run, *command_and_args[1:])
                    continue
                if current_dict['replace']:
                    await message.channel.send(message.content.replace(current_dict['read'], current_dict['write']))
                    continue
                await message.channel.send(current_dict['write'])

    @command(name='pinsert', help=helper.HELP_PINSERT, description=helper.HELP_PINSERT_LONG, aliases=['pizza_insert'])
    async def pinsert(self, ctx: Context, *args):
        """
        Args: type, to_match, response, (replace)
        """
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        fail_embed = self.__embeds.BAD_COMMAND_USAGE("pinsert")
        if len(args) != 2:
            await ctx.send(embed=fail_embed)
            return

        # initialise all variables that will be passed to the json
        time = str(int(ctx.message.created_at.timestamp() * 1000))
        author = str(ctx.message.author.id)
        read = args[0]
        write = args[1]

        # turn replace mode off if the user set it to on
        try:
            PizzaEvalErrorDict.recursion_counter = 0
            evaluated = pizza_eval_read(read, 'a')  # test an evaluation to see if complex read input is valid
        except PizzaEvalUtils.PizzaError as e:
            details = e.args[0]
            await ctx.send(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return

        new_command = {
            "time": time,
            "author": author,
            "read": read,
            "write": write,
        }
        data['p_commands'].append(new_command)

        with open("pizza_database.json", "w") as f2:
            json.dump(data, f2, indent=4)

        await ctx.send(embed=self.__embeds.PIZZA_INSERTED(read, write))
        return

    @command(name='plist', help=helper.HELP_PLIST, description=helper.HELP_PLIST_LONG, aliases=['pizza_list'])
    async def plist(self, ctx: Context, *args):
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) not in (0, 2):
            await ctx.send(embed=self.__embeds.BAD_COMMAND_USAGE("plist"))
            return
        command_list = []
        if args:
            real_args = list(args)
            if real_args[0] not in ['time', 'author', 'read', 'write']:
                await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())
                return

            if args[0] == 'author':
                real_args[1] = str(Utils.ping_to_id(real_args[1]))
                if real_args[1] == 'False':
                    await ctx.send(embed=self.__embeds.BAD_USER_ID(args[1]))
                    return

        for index, current_dict in enumerate(data['p_commands']):
            if not args:
                command_list.append({current_dict['read']: current_dict['write']})
            else:
                if real_args[1] in current_dict[args[0]]:
                    command_list.append({current_dict['read']: current_dict['write']})

        if len(command_list) > self.__config.PIZZA_LIST_LENGTH:
            await ctx.send(embed=self.__embeds.PIZZA_LIST_TOO_LONG())
            return
        if len(command_list) == 0:
            result = "No commands found."
        else:
            print(command_list)
            result = "\n".join(f"{key} -> {value}" for adict in command_list for key, value in adict.items())

        if not args:
            await ctx.send(embed=self.__embeds.PIZZA_LIST(result))
        else:
            await ctx.send(embed=self.__embeds.PIZZA_LIST_FILTERED(result, args[0], args[1]))
        return

    @command(name='pinfo', help=helper.HELP_PINFO, description=helper.HELP_PINFO_LONG, aliases=['pizza_info'])
    async def pinfo(self, ctx: Context, *args) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) not in (1, 2):
            await ctx.send(embed=self.__embeds.BAD_COMMAND_USAGE("pinfo"))
            return

        matching_commands = []
        for current_dict in data['p_commands']:
            if current_dict['write'] == args[0]:
                matching_commands.append(current_dict)

        if len(args) == 1:
            target_command = matching_commands[0]
        elif len(args) == 2:
            try:
                int(args[1])
            except ValueError:
                await ctx.send(embed=self.__embeds.INTEGER_ONLY_HERE(args[1]))
                return
            target_command = matching_commands[int(args[1]) - 1]
        command_editable = deepcopy(target_command)

        command_editable['author'] = f"<@{command_editable['author']}>"
        command_editable['time'] = f"<t:{int(command_editable['time'])//1000}>"
        result = "\n".join(f"{key}: {value}" for key, value in command_editable.items())

        embed = self.__embeds.PIZZA_INFO(result)
        if len(args) == 1 and len(matching_commands) > 1:
            embed.set_footer(text=f"There are {len(matching_commands)} commands with this write result. Did you select the right command?")
        await ctx.send(embed=embed)
        return

    @command(name='premove', help=helper.HELP_PREMOVE, description=helper.HELP_PREMOVE_LONG, aliases=['pizza_remove'])
    async def premove(self, ctx: Context, *args) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) not in (1, 2):
            await ctx.send(embed=self.__embeds.INVALID_ARGUMENTS())
            return

        valid_commands = []

        for current_dict in data['commands']:
            if args[0] == current_dict['write']:
                valid_commands.append(current_dict)

        if len(valid_commands) == 1:
            popped = data['commands'].pop(data['commands'].index(valid_commands[0]))
            await ctx.send(embed=self.__embeds.PREMOVE_REMOVED(popped['write']))
        elif len(valid_commands) > 1:
            if len(args) == 1:
                await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())
                return
            else:
                try:
                    cmd_number = int(args[1])
                except ValueError:
                    await ctx.send(embed=self.__embeds.INTEGER_ONLY_HERE(args[1]))
                    return
                if len(valid_commands) < int(args[1]):
                    await ctx.send(embed=self.__embeds.PREMOVE_NUMBER_LARGER_THAN_AMOUNT_COMMANDS(args[1], len(valid_commands)))
                popped = data['commands'].pop(data['commands'].index(valid_commands[cmd_number-1]))
                await ctx.send(embed=self.__embeds.PREMOVE_REMOVED(popped['write'], cmd_number))
        else:
            await ctx.send(embed=self.__embeds.PREMOVE_NO_COMMAND_FOUND(args[0]))

        with open("pizza_database.json", "w") as f2:
            json.dump(data, f2, indent=4)
        return

    @command(name='ptestcompiler', help=helper.HELP_COMPILER, description=helper.HELP_COMPILER_LONG, aliases=['pizza_test_compiler', 'pcompiler'])
    async def ptestcompiler(self, ctx: Context, *args) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) != 2:
            await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())
            await ctx.send("here's a tip: you need to specify a read and write value")
            await asyncio.sleep(2)
            await ctx.send("and you need to put a spear behind it")
            return

        try:
            PizzaEvalErrorDict.recursion_counter = 0
            evaluated = pizza_eval_read(args[0], args[1])
        except PizzaEvalUtils.PizzaError as e:
            details = e.args[0]
            await ctx.send(embed=self.__embeds.PIZZA_INVALID_INPUT(details['c'], details['e']))
            return
        await ctx.send(evaluated)

def setup(bot):
    bot.add_cog(PizzaRomaniCog(bot))
