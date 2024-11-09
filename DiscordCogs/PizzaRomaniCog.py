import json
from copy import deepcopy
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.PizzaEvaluator import pizza_eval
from Utils.Utils import Utils

helper = Helper()

with open("pizza_database.json", "r") as f:
    data = json.load(f)


class PizzaRomaniCog(Cog):
    """ich ess pizza"""
    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.__bot.user or message.content.lower().startswith('b.pinsert') or not message.content:
            return

        for current_dict in data['commands']:
            send = False

            if current_dict['type'] == 'in':
                if current_dict['read'] in message.content.lower():
                    send = True

            elif current_dict['type'] == 'is':
                if message.content == current_dict['read']:
                    send = True

            elif current_dict['type'] == 'start':
                if message.content.startswith(current_dict['read']):
                    send = True

            elif current_dict['type'] == 'end':
                if message.content.endswith(current_dict['read']):
                    send = True

            elif current_dict['type'] == 'complex':
                if pizza_eval(message.content.lower(), current_dict['read']):
                    send = True
                else:
                    send = False

            if send and (message.guild is None or message.guild.id != 995966314877300737 or any(role.id == 1304403741759508500 for role in message.author.roles)):
                if current_dict['write'].startswith('b.'):  # make it be able to eval its own commands :)
                    command_and_args = current_dict['write'][2:].split(" ")
                    command_to_run = self.__bot.get_command(command_and_args[0])
                    ctx = await self.__bot.get_context(message)
                    await ctx.invoke(command_to_run, *command_and_args[1:])
                    continue
                if current_dict['replace']:
                    await message.channel.send(message.content.replace(current_dict['read'], current_dict['write']))
                    continue
                await message.channel.send(current_dict['write'])

    @command(name='pinsert', help=helper.HELP_PINSERT, description=helper.HELP_PINSERT_LONG, aliases=['pizza_insert'])
    async def pinsert(self, ctx: Context, *args):
        fail_embed = self.__embeds.BAD_COMMAND_USAGE("pinsert")
        if len(args) not in (3, 4):
            await ctx.send(embed=fail_embed)
            return

        time = str(int(ctx.message.created_at.timestamp() * 1000))
        author = str(ctx.message.author.id)
        if args[0] in ["is", "in", "start", "end", "complex"]:
            pizza_type = args[0]
        else:
            await ctx.send(embed=fail_embed)
            return
        read = args[1]
        write = args[2]
        if len(args) == 4:
            replace = True if args[3] == "replace" else False
        else:
            replace = False

        if pizza_type == "complex":
            if not Utils.is_allowed_complex_input(args[1]):
                await ctx.send(embed=fail_embed)
                return

        new_command = {
            "time": time,
            "author": author,
            "type": pizza_type,
            "read": read,
            "write": write,
            "replace": replace
        }

        data['commands'].append(new_command)

        with open("pizza_database.json", "w") as f2:
            json.dump(data, f2, indent=4)

        await ctx.send(embed=self.__embeds.PIZZA_INSERTED(read, write, replace))
        return

    @command(name='plist', help=helper.HELP_PLIST, description=helper.HELP_PLIST_LONG, aliases=['pizza_list'])
    async def plist(self, ctx: Context, *args):
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) not in (0, 2):
            await ctx.send(embed=self.__embeds.BAD_COMMAND_USAGE("plist"))
            return
        command_list = {}
        if args:
            real_args = list(args)
            if real_args[0] not in ['time', 'author', 'read', 'write', 'type', 'replace']:
                await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())
                return

            if args[0] == 'author':
                real_args[1] = str(Utils.ping_to_id(real_args[1]))
                if real_args[1] == 'False':
                    await ctx.send(embed=self.__embeds.BAD_USER_ID(args[1]))
                    return

        for current_dict in data['commands']:
            if not args:
                command_list[current_dict['read']] = current_dict['write']
                if current_dict['replace']:
                    command_list[current_dict['read']] += " (replace)"
            else:
                if real_args[1] in current_dict[args[0]]:
                    command_list[current_dict['read']] = current_dict['write']
                    if current_dict['replace']:
                        command_list[current_dict['read']] += " (replace)"

        if len(command_list) > self.__config.PIZZA_LIST_LENGTH:
            await ctx.send(embed=self.__embeds.PIZZA_LIST_TOO_LONG())
            return
        if len(command_list) == 0:
            result = "No commands found."
        else:
            result = "\n".join(f"{key} -> {value}" for key, value in command_list.items())

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
        for current_dict in data['commands']:
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
            embed.set_footer(text="There is more than 1 command with this write result. Did you select the right command?")
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(PizzaRomaniCog(bot))
