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
        await ctx.send("this command has been decommissioned. please use /alert!")
        async def decommissioned():
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
        await ctx.author.send('I love feet🦶')

    @command(name='clean', help=helper.HELP_CLEAN, description=helper.HELP_CLEAN_LONG)
    async def clean(self, ctx: Context, *args: str) -> None:
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        await ctx.send("this command has been decommissioned. please use /clean!")
        return
        async def decommissioned():
            limit = 20
            who = "all"
            valid_targets = ("all", "bot", "user", "saul", "any")
            if args:
                for arg in args:
                    if arg.isdigit():
                        limit = int(arg)
                    elif arg.lower() in valid_targets:
                        who = arg.lower()
                    else:
                        await ctx.send(embed=self.__embeds.BAD_CLEAN_INPUT(arg))

            if limit > self.__config.CLEAN_AMOUNT:
                await ctx.send(embed=self.__embeds.TOO_MANY_CLEAN_QUERIES(limit))
                return

            def should_delete(msg_to_delete):
                if who == "any":
                    return True
                if who == "saul" and message.author.id == 1012755944846938163:
                    return True
                if who in ("bot", "all") and message.author.id == ctx.bot.user.id:
                    return True
                if who in ("user", "all") and msg_to_delete.content.startswith(self.__config.BOT_PREFIX):
                    return True
                return False

            inspect_amount = limit if who == "any" else self.__config.CLEAN_AMOUNT
            to_delete: list = []

            async for message in ctx.channel.history(limit=inspect_amount):
                if len(to_delete) >= limit:
                    break

                if should_delete(message):
                    to_delete.append(message)

            if to_delete:
                from datetime import datetime, timedelta, timezone

                two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)

                bulk_deletable = [m for m in to_delete if m.created_at > two_weeks_ago]
                manual_deletable = [m for m in to_delete if m.created_at <= two_weeks_ago]

                if bulk_deletable:
                    await ctx.channel.delete_messages(bulk_deletable, reason="b.clean")

                if manual_deletable:
                    for i, msg in enumerate(manual_deletable):
                        await msg.delete()
                        if (i+1) % 5 == 0:
                            await asyncio.sleep(1)

            await ctx.send(embed=self.__embeds.CLEANED(limit, len(to_delete), who, inspect_amount), delete_after=10)

    @command(name="blud", help=helper.HELP_BLUD)
    async def blud(self, ctx: Context, *args):
        await ctx.send("blud")

    # this command only exists to generate a help function for it
    @command(name='riichi_hand', help=helper.HELP_RIICHI, description=helper.HELP_RIICHI_LONG)
    async def riichi_hand(self, ctx: Context):
        await ctx.send("this command only exists to create a help function. please use the slash command with the same name")


def setup(bot):
    bot.add_cog(MiscCog(bot))
