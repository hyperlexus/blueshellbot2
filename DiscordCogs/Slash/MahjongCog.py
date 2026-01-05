import discord

from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Cog, slash_command
from discord import ApplicationContext, Option
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.riichi.RiichiLogic import get_tiles_from_hand_string
from Utils.riichi.RiichiUtils import RiichiError

helper = Helper()

class MahjongCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()

    @slash_command(name="riichi_hand", description="takes a custom input and makes a riichi hand with it. check b.help riichi_hand for more info")
    async def riichi_hand(self, ctx: ApplicationContext, hand: Option(str, "input your hand string here. no spaces and no commas!")):
        try:
            image_bytes = get_tiles_from_hand_string(hand)
        except RiichiError as error:
            await ctx.respond(embed=self.__embeds.RIICHI_HAND_ERROR(error))
            return

        filename = 'haaaaaaaaaaaaaaand.png'
        discord_file = discord.File(fp=image_bytes, filename='haaaaaaaaaaaaaaand.png')

        embed = self.__embeds.RIICHI_HAND_EMBED()
        embed.set_image(url=f"attachment://{filename}")

        await ctx.respond(file=discord_file, embed=embed)


def setup(bot):
    bot.add_cog(MahjongCog(bot))
