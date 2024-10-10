import asyncio
import inspect
import os
import sys
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
helper = Helper()

class ModCog(Cog):
    """Cog for moderation commands only usable by bot admins"""
    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @command(name='restart', help=helper.HELP_RESTART, description=helper.HELP_RESTART_LONG, aliases=['reboot', 'kill'])
    async def restart(self, ctx: Context) -> None:
        bot_admins = self.__config.BOT_ADMINS.split(",")
        if str(ctx.author.id) not in bot_admins:
            embed = self.__embeds.MISSING_PERMISSIONS("restart")
            await ctx.send(embed=embed)
            return
        await ctx.send("restarting bot, please be patient.")
        os.chdir(self.__config.BAT_PATH)
        os.startfile("runbot.bat")
        stop_music_command = self.__bot.get_command('stop')
        await stop_music_command(ctx)
        await asyncio.sleep(2)
        await self.__bot.close()
        sys.exit(69)

    @command(name='ban', help=helper.HELP_BAN, description=helper.HELP_BAN_LONG)
    async def ban(self, ctx: Context, *args) -> None:
        os.chdir(self.__config.PROJECT_PATH)
        bot_admins = self.__config.BOT_ADMINS.split(",")
        if str(ctx.author.id) not in bot_admins:
            embed = self.__embeds.MISSING_PERMISSIONS("ban")
            await ctx.send(embed=embed)
            return

        try:
            to_ban = int(args[0])
            if to_ban // 1_000_000_000_000 < 1:
                embed = self.__embeds.BAD_USER_ID(args[0])
                await ctx.send(embed=embed)
                return
            to_ban = str(to_ban)
        except ValueError:
            embed = self.__embeds.BAD_USER_ID(args[0])
            await ctx.send(embed=embed)
            return

        if to_ban in bot_admins:
            embed = self.__embeds.INVALID_BAN_COMMAND()
            await ctx.send(embed=embed)
            return

        username = str(self.__bot.get_user(int(to_ban)))[:-2]

        with open("./banlist.txt", "r+") as file:
            banlist = file.read().splitlines()
            if to_ban not in banlist:
                banlist.append(to_ban)
                embed = self.__embeds.SUCCESSFUL_BAN(username)
            else:
                embed = self.__embeds.SUCCESSFUL_UNBAN(username)
                banlist[:] = (uid for uid in banlist if uid != to_ban)

        with open("./banlist.txt", "w") as file:
            for i in banlist:
                file.write(f"{i}\n")

        await ctx.send(embed=embed)
        return

    @command(name='force_embed', help=helper.HELP_FORCE_EMBED, description=helper.HELP_FORCE_EMBED_LONG)
    async def force_embed(self, ctx: Context, *args) -> None:
        embed_to_force = None
        if len(args) != 1:
            embed = self.__embeds.INCORRECT_FORCE_EMBED()
            await ctx.send(embed=embed)
            return

        bot_admins = self.__config.BOT_ADMINS.split(",")
        if str(ctx.author.id) not in bot_admins:
            embed = self.__embeds.MISSING_PERMISSIONS("force_embed")
            await ctx.send(embed=embed)
            return

        all_embeds = [embed_name for embed_name in dir(self.__embeds)
                      if callable(getattr(self.__embeds, embed_name))
                      and not embed_name.startswith("_")]

        if args[0] == "list":
            output = "All available embeds: \n"
            for number, embed in enumerate(all_embeds):
                output += f"{number+1}. {embed} \n"
            await ctx.send(output)
            return

        if args[0].isdigit():
            embed_index = int(args[0]) - 1
            if 0 <= embed_index < len(all_embeds):
                embed_to_force = all_embeds[embed_index]
        else:
            if args[0].upper() in all_embeds:
                embed_to_force = args[0].upper()
            else:
                embed = self.__embeds.INCORRECT_FORCE_EMBED()
                await ctx.send(embed=embed)
                return

        embed_method = getattr(self.__embeds, embed_to_force)

        sig = inspect.signature(embed_method).parameters
        call_args = []

        for i in range(len(sig)):
            call_args.append(f"default_forced_arg_{i}")

        embed = embed_method(*call_args)
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(ModCog(bot))
