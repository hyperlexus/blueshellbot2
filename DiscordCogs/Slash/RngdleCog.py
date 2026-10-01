import json
from datetime import datetime, time, timezone
from discord.ext import tasks

from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Cog, slash_command
from discord import ApplicationContext, option
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.rngdle_scraper.scrape_and_rape import scrape_rngdle_today, rape_lightweight

def is_utc_today(date: datetime) -> bool:
    return datetime.now(timezone.utc).date() == date.date()

def make_yesterday_summary(data) -> str:
    msg = "rngdle reset!\n"
    for uid, roll in data["rolled_today"].items():
        msg += f"<@{uid}> rolled **{roll}**\n"
    return msg

class RngdleCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        with open("Storage/rngdle.json", "r") as f:
            data = json.load(f)

        data.setdefault("participants", {})
        data.setdefault("rolled_today", {})
        data.setdefault("last_reset", "")

        with open("Storage/rngdle.json", "w") as f:
            json.dump(data, f, indent=4)
        self.check_new_rolls.start()

    @slash_command(name="rngdle_sign_up", description="add your username to the daily checks", guild_ids=[995966314877300737])
    @option(name="username", description="your rngdle username, such as rngdle.com/u/hyperlexus")
    async def rngdle_sign_up(self, ctx: ApplicationContext, username: str):
        await ctx.defer()
        with open("Storage/rngdle.json", "r") as f:
            data = json.load(f)

        data["participants"][f"{ctx.author.id}"] = username
        with open("Storage/rngdle.json", "w") as f:
            json.dump(data, f, indent=4)
        return await ctx.respond(f"signed up {username} with id {ctx.author.id}. to verify, your last roll was {await rape_lightweight(username, ctx.author.id)}")

    @tasks.loop(seconds=600)
    async def check_new_rolls(self) -> None:
        with open("Storage/rngdle.json", "r") as f:
            data = json.load(f)
        today_utc_str = datetime.now(timezone.utc).date().isoformat()
        last_reset = data.get("last_reset")

        if last_reset != today_utc_str:
            channel = self.__bot.get_channel(1555281590211444847)
            await channel.send(make_yesterday_summary(data))
            data["rolled_today"] = {}
            data["last_reset"] = today_utc_str
            with open("Storage/rngdle.json", "w") as f:
                json.dump(data, f, indent=4)
            return

        user_ids = data["participants"]
        rolled_today = set(str(uid) for uid in data["rolled_today"].keys())

        for user_id_str, username in user_ids.items():
            if user_id_str in rolled_today:
                continue
            else:
                output_text, date = await scrape_rngdle_today(username, user_id_str)
                roll = output_text.split("\n")[1].replace("# ", "").replace("\n\n", "")
                if is_utc_today(date):
                    data["rolled_today"][user_id_str] = roll
                    channel = self.__bot.get_channel(1555281590211444847)
                    await channel.send(output_text)
        with open(f"Storage/rngdle.json", "w") as f:
            json.dump(data, f, indent=4)
        return

    @check_new_rolls.before_loop
    async def before_check_new_rolls(self):
        await self.__bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RngdleCog(bot))