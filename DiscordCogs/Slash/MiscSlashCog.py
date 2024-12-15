import math
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
        await ctx.respond(embed=self.__embeds.UPTIME(str(datetime.now() - blueshell_entire_bot_startup_timestamp)[:-7]))

    @slash_command(name='festgelegte_vertrege', description='vertrag mit der bank ausrechnen')
    async def vertrege(self, ctx: ApplicationContext,
                       geld: Option(int, "Geld"),
                       rate: Option(int, "Rückzahlrate in %")
                       ) -> None:
        if rate > 100 or rate < 1:
            await ctx.respond("prozent von 1 bis 100")
        if geld < 1000:
            await ctx.respond("1000 ist untergrenze für geld bratan")
        if geld > 1000000:
            await ctx.respond("du kannst dir nicht mehr als 1e6 geld leihen")

        def regerplatz(geld2, rate2):
            return math.ceil(geld2 ** 0.5 / 10) / (4 * rate2)

        result = geld, rate, int(regerplatz(geld, rate)*100), int(geld*(1+regerplatz(geld, rate)))
        await ctx.respond(embed=self.__embeds.FESTGELEGTE_VERTREGE_EMBED(result[0], result[1], result[2], result[3]))
        return


def setup(bot):
    bot.add_cog(MiscSlashCog(bot))
