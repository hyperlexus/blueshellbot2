import asyncio
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
        bot_admins = self.__config.BOT_ADMINS.split(",")
        if str(ctx.author.id) not in bot_admins:
            embed = self.__embeds.MISSING_PERMISSIONS("ban")
            await ctx.send(embed=embed)
            return
        try:
            to_ban = int(args[0])
        except ValueError:
            embed = self.__embeds.BAD_USER_ID(args[0])
            await ctx.send(embed=embed)
            return
        os.chdir(self.__config.PROJECT_PATH)
        with open("./banlist.txt", "a") as file:
            await ctx.send(str(to_ban))
            file.write(str(to_ban))
            await ctx.send("successful")



def setup(bot):
    bot.add_cog(ModCog(bot))
