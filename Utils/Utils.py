import os
import re
import asyncio
from datetime import datetime, timedelta
from functools import wraps, partial
from forbiddenfruit import cursed
from discord import ApplicationContext
from discord.ext.commands import check
from Config.Configs import BConfigs
from Config.Embeds import BEmbeds

config = BConfigs()
embeds = BEmbeds()


class Utils:
    time_units: dict[str, int] = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    @classmethod
    def format_time(cls, duration) -> str:
        if not duration:
            return "00:00"

        hours = duration // 60 // 60
        minutes = duration // 60 % 60
        seconds = duration % 60

        return "{}{}{:02d}:{:02d}".format(hours if hours else "", ":" if hours else "", minutes, seconds)

    @classmethod
    def check_if_banned(cls, user, path) -> bool:
        banned_ids = []
        with open(os.path.join(path, "Storage/banlist.txt"), "r") as file:
            for line in file:
                try:
                    banned_ids.append(int(line))
                except ValueError:
                    print("something went past the checker in the ban command, and a character is in here")
                    return False
        return True if user in banned_ids else False

    @classmethod
    def convert_relative_time_to_s(cls, time_str: str) -> int:
        time_blocks: list = []
        current_time_block: str = ""
        total_seconds: int = 0

        for char in time_str:
            if char not in cls.time_units.keys() and not char.isdigit(): raise ValueError(
                f"incorrectly submitted alert: {time_str}")
            current_time_block += char
            if char in cls.time_units.keys():
                time_blocks.append(current_time_block)
                current_time_block = ""

        def convert_block_to_seconds(time_block: str) -> int:
            unit = time_block[-1]
            try:
                amount_units = int(time_block[:-1])
            except ValueError:
                raise ValueError(f"incorrectly submitted alert: {time_str}")
            return amount_units * cls.time_units[unit]

        for block in time_blocks:
            total_seconds += convert_block_to_seconds(block)
        return total_seconds

    @classmethod
    def convert_absolute_time_to_s(cls, time_str: str) -> int:
        def convert_T_to_D(t_time_str: str) -> str:
            t_time_str = t_time_str.strip()[1:]
            units = [int(u) for u in t_time_str.split(':')]

            if len(units) not in (2, 3): raise ValueError(f"incorrect alert t-format: {t_time_str}")

            hour, minute = units[0], units[1]
            second = units[2] if len(units) == 3 else 0

            now = datetime.now()

            target_date = (now + timedelta(days=1)).date() if now.hour > hour else now.date()
            target_datetime = datetime.combine(target_date, datetime.min.time()).replace(hour=hour, minute=minute, second=second)

            return f"d{target_datetime.strftime('%Y-%m-%d;%H:%M:%S')}"

        if time_str.startswith("t"):
            time_str = convert_T_to_D(time_str)

        obj = datetime.strptime(time_str, "d%Y-%m-%d;%H:%M:%S")
        return int((obj - datetime.now()).total_seconds())

    @classmethod
    def convert_seconds_to_time_info(cls, seconds: int) -> str:
        output: str = ""
        for unit_name, unit_value in reversed(cls.time_units.items()):
            with cursed(int, "custom_round_down_with_return_remainder", custom_round_down_with_return_remainder):
                amount, seconds = seconds.custom_round_down_with_return_remainder(unit_value)  # wahrlich cursed

                if amount > 0:
                    output += f"{amount}{unit_name}"
        return output

    @classmethod
    def is_url(cls, string: str) -> bool:
        regex = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        if re.search(regex, string):
            return True
        else:
            return False

    @classmethod
    def ping_to_id(cls, user_id) -> (int | bool):
        """Turns a ping to a user id, and keeps the id if it already is an id"""
        if user_id.startswith('<@') and user_id.endswith('>'):
            user_id = user_id[2:-1]
        try:
            user_id = int(user_id)
        except ValueError:
            return False
        if not (user_id // 1_000_000_000_000 < 1):
            return user_id
        return False

    @classmethod
    def helper_calcdifftime(cls, end_str: str) -> str:
        difference = datetime.strptime(end_str, '%Y-%m-%dZ%H:%M:%S') - datetime.now()
        total_seconds = int(difference.total_seconds())
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{int(days):02d}d {int(hours):02d}h {int(minutes):02d}m"

    @classmethod
    def convert_rules_to_list(cls, rules: str | None, mode: str) -> list:
        if rules is None:
            return []
        if rules.count(",") == 0:
            try:
                rules = [int(rules)]
                if rules[0] < 1 or mode == "div" and rules[0] < 2:
                    return [-1]
                return rules
            except ValueError:
                return [-1]
        rules = rules.split(",")
        if rules == ['']:
            return []
        for i in range(len(rules)):
            try:
                rules[i] = int(rules[i])
                if rules[i] < 1 or mode == "div" and rules[i] < 2:
                    return [-1]
            except ValueError:
                return [-1]
        return rules

def run_async(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        partial_func = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, partial_func)
    return run

def is_not_banned(storage_path: str = config.PROJECT_PATH):
    async def predicate(ctx) -> bool:
        banlist_path = os.path.join(storage_path, "Storage/banlist.txt")

        if not os.path.exists(banlist_path): return True  # i guess bro

        user_id = ctx.author.id

        with open(banlist_path, "r") as f:
            for line in f:
                line_str = line.strip()
                if not line_str: continue
                try:
                    if user_id == int(line_str):
                        if isinstance(ctx, ApplicationContext):
                            await ctx.respond(embed=embeds.BANNED())
                        else:
                            await ctx.send(embed=embeds.BANNED())
                        return False
                except ValueError:
                    print(f"bad line in banlist.txt: {line_str}")
                    continue

        return True
    return check(predicate)

def custom_round_down_with_return_remainder(self: int, unit_value: int) -> tuple[int, int]:
    quotient = self // unit_value
    remainder = self % unit_value
    return quotient, remainder


def is_bot_admin(bot_admins = config.BOT_ADMINS):
    async def predicate(ctx) -> bool:
        admin_list = bot_admins.split(",")
        if str(ctx.author.id) not in admin_list:
            await ctx.send(embed=embeds.MISSING_PERMISSIONS())
            return False
        return True
    return check(predicate)