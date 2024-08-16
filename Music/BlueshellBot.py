import asyncio
from asyncio import AbstractEventLoop
import discord
from datetime import datetime
from discord import Guild, Status, Game, Message
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from Config.Configs import BConfigs
from discord.ext.commands import Bot, Context
from Config.Messages import Messages
from Config.Embeds import BEmbeds


def helper_calcdifftime(end_str, format_str='%Y-%m-%dZ%H:%M:%S'):
    start_dt = datetime.now()
    end_dt = datetime.strptime(end_str, format_str)
    difference = end_dt - start_dt
    total_seconds = int(difference.total_seconds())
    days = total_seconds // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    result = f"{int(days):02d}d {int(hours):02d}h {int(minutes):02d}m"
    return result


class BlueshellBot(Bot):
    def __init__(self, listingSlash: bool = False, *args, **kwargs):
        """If listing Slash is False then the process is just a Player Process, should not interact with discord commands"""
        super().__init__(*args, **kwargs)
        self.__listingSlash = listingSlash
        self.__configs = BConfigs()
        self.__messages = Messages()
        self.__embeds = BEmbeds()
        self.remove_command("help")

    @property
    def listingSlash(self) -> bool:
        return self.__listingSlash

    def startBot(self) -> None:
        """Blocking function that will start the bot"""
        if self.__configs.BOT_TOKEN == '':
            print('bruh put the fucking token this has happened 8 times now')
            exit()

        super().run(self.__configs.BOT_TOKEN, reconnect=True)

    async def startBotCoro(self, loop: AbstractEventLoop) -> None:
        """Start a bot coroutine, does not wait for connection to be established"""
        task = loop.create_task(self.__login())
        await task
        loop.create_task(self.__connect())

    async def __login(self):
        """Coroutine for bot login"""
        await self.login(token=self.__configs.BOT_TOKEN)

    async def __connect(self):
        """Coroutine for bot connection"""
        await self.connect(reconnect=True)

    async def change_status(self):
        while True:
            # line to change when prim gives you the time of arrival :)
            # await self.change_presence(status=Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"{helper_calcdifftime('2024-09-07Z15:00:00')}"))
            await self.change_presence(status=Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"prefix: '{self.__configs.BOT_PREFIX}'"))
            await asyncio.sleep(1)

    async def on_ready(self):
        if self.__listingSlash:
            print(self.__messages.STARTUP_MESSAGE)
        await self.change_presence(status=Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=f"prefix: '{self.__configs.BOT_PREFIX}'"))
        if self.__listingSlash:
            print(self.__messages.STARTUP_COMPLETE_MESSAGE)
        await self.loop.create_task(self.change_status())

    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = self.__embeds.MISSING_ARGUMENTS()
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = self.__embeds.COMMAND_NOT_FOUND()
            await ctx.send(embed=embed)

        else:
            print(f'Command has thrown an error -> {error}')
            embed = self.__embeds.UNKNOWN_ERROR()
            await ctx.send(embed=embed)

    async def process_commands(self, message: Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=Context)

        if ctx.valid and not message.guild:
            return

        await self.invoke(ctx)


class Context(Context):
    bot: BlueshellBot
    guild: Guild
