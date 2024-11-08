import asyncio
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils
import Utils.Kana as Kana

helper = Helper()

class JapaneseCog(Cog):
    """Class for all commands relating to japanese queries"""

    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    # testing
    @command(name="convkana", help=helper.HELP_CONVKANA, description=helper.HELP_CONVKANA_LONG, aliases=['conv'])
    async def convkana(self, ctx: Context, *args) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if len(args) != 2:
            await ctx.send(embed=self.__embeds.BAD_COMMAND_USAGE('convkana'))
            return
        output = Kana.conv_multiple_kana(args[0], args[1])
        await ctx.send(embed=self.__embeds.KANA_CONVERTED_EMBED(args[1], output[0], args[0], output[1]))
        return

    @command(name="kanagame", help=helper.HELP_KANA_GAME, description=helper.HELP_KANA_GAME_LONG, aliases=['kgame'])
    async def kanagame(self, ctx: Context, *args) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        pass

    @command(name="blud")
    async def blud(self, ctx: Context, *args):
        await ctx.send("blud")

def setup(bot):
    bot.add_cog(JapaneseCog(bot))
