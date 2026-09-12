import asyncio
import contextlib
import io
import trace
from random import random

import discord
from discord import Member
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog, has_permissions
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils, is_not_banned

helper = Helper()

class MiscCog(Cog):
    """Class to listen to commands of type Misc"""

    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @command(name='wahl', help=helper.HELP_WAHL, description=helper.HELP_WAHL_LONG, aliases=['wahlkommission'])
    @is_not_banned()
    async def wahlkommission(self, ctx: Context) -> None:
        result = round(random() * 100)
        if result == 69:
            result = (f"{str(result)}. 恭喜你獲得傳奇號碼69！無論您是擲骰子、轉動輪盤，還是只是碰巧發現了這個標誌性數字，今天都是您的幸運"
                      f"日！69 不只是一個普通的數字──它是平衡、二元性和樂趣的象徵。擁抱 69 的俏皮能量！它提醒我們不要把生活看得太嚴肅，並在"
                      f"意外中尋找快樂。與朋友分享您的好運，為隨機性的力量乾杯，或只是沉浸在數位勝利的榮耀中。請記住，69 不只是一個數字，更是"
                      f"一種心態。在您所做的每一件事中都保持 69 精神，誰知道您還會遇到什麼其他令人驚奇的事情？為你和神奇的數字69乾杯！願您的好"
                      f"運繼續，您的慶祝活動充滿歡笑和美好氛圍。\nInspiriert von maggda auf whatsapp")
        if result == 100:
            result = f"{str(result)}, sie haben die höchste mögliche zahl, die wahlkommission sagt auf jeden fall ja, hurruh"
        if result == 0:
            result = f"{str(result)}, sie ham gekackt. sie können einfach garnix; sie blöder kackspast. gehen sie sich begraben."

        await ctx.send(embed=self.__embeds.WAHLKOMMISSION(result))

    @command(name='feet', help=helper.HELP_FEET, description=helper.HELP_FEET_LONG)
    async def feet(self, ctx: Context) -> None:
        await ctx.author.send('I love feet🦶')

    @command(name="blud", help=helper.HELP_BLUD)
    async def blud(self, ctx: Context, *args):
        await ctx.send("blud")

    # this command only exists to generate a help function for it
    @command(name='riichi_hand', help=helper.HELP_RIICHI, description=helper.HELP_RIICHI_LONG)
    async def riichi_hand(self, ctx: Context):
        await ctx.send("this command only exists to create a help function. please use the slash command with the same name")

    @command(name='kick')
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, *, reason: str):
        try:
            await member.kick(reason="blud.")
            await ctx.send(f"{member.display_name} has been kicked.")
        except:
            pass


    @command(name='eval')
    async def blueshell_eval(self, ctx: Context, *, body: str) -> discord.Message:
        if ctx.message.author.id not in (640985620948189186, 422800248935546880): return await ctx.send(f"you can't do this, {ctx.message.author.display_name}.")
        if "```py" not in body:
            return await ctx.send("error: missing `\\`\\`\\`py` format.")

        code = body.split("```py")[1].split("```")[0].strip()
        stdout = io.StringIO()

        env = {
            'ctx': ctx,
            'bot': self.__bot,
            'self': self,
            'author': ctx.author,
            'channel': ctx.channel,
            'guild': ctx.guild,
        }

        try:
            with contextlib.redirect_stdout(stdout):
                exec(code, env)

            output = stdout.getvalue()
            if not output:
                output = "Code did not print anything."

            return await ctx.send(f"Evaluated output:\n```py\n{output}\n```")

        except Exception as e:
            return await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")


def setup(bot):
    bot.add_cog(MiscCog(bot))
