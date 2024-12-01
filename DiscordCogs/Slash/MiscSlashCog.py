from datetime import datetime
from Music.BlueshellBot import BlueshellBot
from Music.BlueshellBot import blueshell_entire_bot_startup_timestamp
from discord import ApplicationContext, Option, OptionChoice
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs

helper = Helper()

class MiscSlashCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()

    @slash_command(name='uptime', description="get time since last restart")
    async def uptime(self, ctx: ApplicationContext) -> None:
        await ctx.respond(str(datetime.now() - blueshell_entire_bot_startup_timestamp)[:-6])

def setup(bot):
    bot.add_cog(MiscSlashCog(bot))
