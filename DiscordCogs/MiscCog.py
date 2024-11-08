import asyncio
from random import random
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils
helper = Helper()

class MiscCog(Cog):
    """Class to listen to commands of type Misc"""

    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @command(name='wahl', help=helper.HELP_WAHL, description=helper.HELP_WAHL_LONG, aliases=['wahlkommission'])
    async def wahlkommission(self, ctx: Context) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
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

    @command(name='alert', help=helper.HELP_ALERT, description=helper.HELP_ALERT_LONG, aliases=['remindme', 'timer', 'reminder'])
    async def alert(self, ctx: Context, time_str: str, *args: str) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return

        other_user, text = False, None
        if args:
            text = " ".join(args[1:]) if len(args) > 1 else None
            user_id = Utils.ping_to_id(args[0])
            if not user_id:
                await ctx.send(embed=self.__embeds.BAD_USER_ID(args[0]))
                return
            if user_id != args[0]:
                other_user = True

        new_time_str = Utils.seconds_until(time_str[1:]) if time_str.startswith('t') else time_str
        seconds = Utils.convert_to_s(new_time_str)
        if seconds is None:
            await ctx.send(embed=self.__embeds.BAD_ALERT(time_str))
            return

        await ctx.send(embed=self.__embeds.ALERT_SET(new_time_str))

        await asyncio.sleep(seconds)

        if other_user:
            await ctx.send(f'<@{user_id}>')
            await ctx.send(embed=self.__embeds.ALERT_DONE(new_time_str, text or "", other_user))
        else:
            await ctx.reply(embed=self.__embeds.ALERT_DONE(new_time_str, text or "", other_user))

    @command(name='feet', help=helper.HELP_FEET, description=helper.HELP_FEET_LONG)
    async def feet(self, ctx: Context) -> None:
        await ctx.send('I love feet🦶')

    @command(name='clean', help=helper.HELP_CLEAN, description=helper.HELP_CLEAN_LONG)
    async def clean(self, ctx: Context, *args: str) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        number_set, limit, c, who = False, 20, 0, "all"  # innit bruv
        if not args == ():
            for i in args:
                try:
                    limit = int(i)
                    number_set = True
                except ValueError:
                    pass
                if not number_set:
                    if type(i) == str and i in ("all", "bot", "user", "saul", "any"):
                        who = i
                    else:
                        await ctx.send(embed=self.__embeds.BAD_CLEAN_INPUT(args))
                        return

        if limit > self.__config.CLEAN_AMOUNT:
            await ctx.send(embed=self.__embeds.TOO_MANY_CLEAN_QUERIES(limit))
            return

        if who == "any":
            inspect_amount = limit
        else:
            inspect_amount = self.__config.CLEAN_AMOUNT

        async for message in ctx.channel.history(limit=inspect_amount):
            if c-1 >= limit:
                break
            deleted = False
            if who == "any":
                await message.delete()
                deleted = True
            if who == "saul" and not deleted:
                if message.author.id == 1012755944846938163:
                    await message.delete()
                    deleted = True
            if who in ("bot", "all") and not deleted:
                if message.author.bot:
                    await message.delete()
                    deleted = True
            if who in ("user", "all") and not deleted:
                if message.content.startswith(f"{self.__config.BOT_PREFIX}"):
                    await message.delete()
                    deleted = True
            if not deleted:
                continue
            c += 1

            if c % 5 == 0:
                await asyncio.sleep(1)

        if c == 0:
            c = 1

        await ctx.send(embed=self.__embeds.CLEANED(limit, c-1, who, inspect_amount), delete_after=10)

def setup(bot):
    bot.add_cog(MiscCog(bot))
