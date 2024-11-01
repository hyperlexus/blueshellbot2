import asyncio
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils
import Utils.Kana
helper = Helper()

class JapaneseCog(Cog):
    """Class for all commands relating to japanese queries"""

    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

def setup(bot):
    bot.add_cog(JapaneseCog(bot))
