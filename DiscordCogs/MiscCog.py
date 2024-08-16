import asyncio
import subprocess
import sys
from datetime import datetime
from random import randint, random
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
helper = Helper()

def convert_to_s(time: str):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    time_value = int(time[:-1])
    time_unit = time[-1]

    if time_unit in units:
        return time_value * units[time_unit]
    else:
        return None

def seconds_until(time_str: str):
    try:
        if ':' in time_str:
            time_array = time_str.split(':')
        else:
            return False
        time_int: int = 0
        for i in range(len(time_array)):
            time_array[i] = int(time_array[i])
            time_int += time_array[i] * 3600 / (60**i)
        time_int = int(time_int)
    except ValueError:
        return False
    now = datetime.now()
    now_h, now_m, now_s = now.hour, now.minute, now.second
    now_seconds = now_h * 3600 + now_m * 60 + now_s
    try:
        time_int = (time_int - now_seconds) % 86400
    except ValueError:
        return False
    time = f"{time_int}s"
    return time

class MiscCog(Cog):
    """Class to listen to commands of type Misc"""

    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @command(name='random', help=helper.HELP_RANDOM, description=helper.HELP_RANDOM_LONG, aliases=['rand'])
    async def random(self, ctx: Context, arg: str) -> None:
        try:
            arg = int(arg)

        except:
            embed = self.__embeds.ERROR_NUMBER()
            await ctx.send(embed=embed)
            return None

        if arg < 1:
            a = arg
            b = 1
        else:
            a = 1
            b = arg

        x = randint(a, b)
        embed = self.__embeds.RANDOM_NUMBER(a, b, x)
        await ctx.send(embed=embed)

    @command(name='wahl', help=helper.HELP_WAHL, description=helper.HELP_WAHL_LONG, aliases=['wahlkommission'])
    async def wahlkommission(self, ctx: Context) -> None:
        x = random()
        result = round(x * 100)
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

        embed = self.__embeds.WAHLKOMMISSION(result)
        await ctx.send(embed=embed)

    @command(name='alert', help=helper.HELP_ALERT, description=helper.HELP_ALERT_LONG, aliases=['remindme', 'timer', 'reminder'])
    async def alert(self, ctx: Context, time_str: str, *args: str) -> None:
        if ctx.author.id != 422800248935546880:
            await ctx.send("hörn sie auf mit den scheis alerts sie nazi")
            return
        other_user = True
        if not args == ():
            user_id = args[0]
            if len(args) > 1:
                text = args[1]
            try:
                if user_id[0] == '<':
                    user_id = user_id[2:-1]
                try:
                    user_id = int(user_id)
                except ValueError:
                    text = user_id
                    other_user = False
            except ValueError:
                embed = self.__embeds.BAD_USER_ID(user_id)
                await ctx.send(embed=embed)
                return
        else:
            other_user = False

        try:
            new_time_str = False
            if time_str[0] == 't':
                new_time_str = seconds_until(time_str[1:])
                if not new_time_str:
                    embed = self.__embeds.BAD_ALERT(time_str)
                    await ctx.send(embed=embed)
                    return
            if not new_time_str:
                new_time_str = time_str
            seconds = convert_to_s(new_time_str)

            if seconds is None:
                embed = self.__embeds.BAD_ALERT(time_str)
                await ctx.send(embed=embed)
                return

            embed = self.__embeds.ALERT_SET(new_time_str)
            await ctx.send(embed=embed)

            await asyncio.sleep(seconds)
            if len(args) == 2 or len(args) == 1 and not other_user:
                embed = self.__embeds.ALERT_DONE(new_time_str, text, other_user)
            elif len(args) < 2:
                embed = self.__embeds.ALERT_DONE(new_time_str)

            if other_user:
                await ctx.send(f'<@{user_id}>')
                await ctx.send(embed=embed)
            else:
                await ctx.reply(embed=embed)

        except IndexError as i:
            await ctx.send(i)
        except Exception as e:
            embed = self.__embeds.BAD_ALERT(new_time_str)
            await ctx.send(embed=embed)

    @command(name='clean', help=helper.HELP_CLEAN, description=helper.HELP_CLEAN_LONG, aliases=[''])
    async def clean(self, ctx: Context, *args: str) -> None:
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
                        embed = self.__embeds.BAD_CLEAN_INPUT(args)
                        await ctx.send(embed=embed)
                        return

        if limit > self.__config.CLEAN_AMOUNT:
            embed = self.__embeds.TOO_MANY_CLEAN_QUERIES(limit)
            await ctx.send(embed=embed)
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

        if who == "bot":
            last_message = await ctx.channel.history(limit=1).flatten()
            await last_message[0].delete()

        if c == 0:
            c = 1

        embed = self.__embeds.CLEANED(limit, c-1, who, inspect_amount)
        await ctx.send(embed=embed, delete_after=10)

    @command(name='choose', help=helper.HELP_CHOOSE, description=helper.HELP_CHOOSE_LONG, aliases=['pick'])
    async def choose(self, ctx: Context, *args: str) -> None:
        try:
            user_input = " ".join(args)
            items = user_input.split(sep=',')

            index = randint(0, len(items) - 1)

            embed = self.__embeds.CHOSEN_THING(items[index])
            await ctx.send(embed=embed)
        except:
            embed = self.__embeds.BAD_CHOOSE_USE()
            await ctx.send(embed=embed)

    @command(name='restart', help=helper.HELP_RESTART, description=helper.HELP_RESTART_LONG, aliases=['reboot', 'kill'])
    async def restart(self, ctx: Context) -> None:
        if ctx.author.id != 422800248935546880:
            await ctx.send("You are not the owner of this bot and are not permitted to run this command.")
            return
        await ctx.send("restarting bot, please be patient")
        print(sys.executable)

        await self.__bot.close()
        await asyncio.sleep(2)

        process = subprocess.Popen(
            ["cmd.exe", "/c", "start", "runbot.bat"],
            cwd="C:\\Users\\HyperLexus\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )
        return_code = process.wait()
        if return_code != 0:
            print(f"An error occurred: {return_code}")
        sys.exit(0)

def setup(bot):
    bot.add_cog(MiscCog(bot))
