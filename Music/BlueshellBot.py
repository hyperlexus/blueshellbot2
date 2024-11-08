import asyncio
from asyncio import AbstractEventLoop
from datetime import datetime
import discord
from discord import Guild, Status, Game, Message
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, ExpectedClosingQuoteError, UnexpectedQuoteError, BadArgument
from Config.Configs import BConfigs
from Config.Messages import Messages
from Config.Embeds import BEmbeds
from Utils.Utils import Utils


class BlueshellBot(Bot):
    def __init__(self, listingSlash: bool = False, *args, **kwargs):
        """If listing Slash is False then the process is just a Player Process, should not interact with discord commands"""
        super().__init__(*args, **kwargs)
        self.__listingSlash = listingSlash
        self.__configs = BConfigs()
        self.__messages = Messages()
        self.__embeds = BEmbeds()
        self.__bot = Bot()
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
            await self.change_presence(status=Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"{Utils.helper_calcdifftime('2024-09-03Z19:10:00')}"))
            await asyncio.sleep(1)

    async def on_ready(self):
        if self.__listingSlash:
            print(self.__messages.STARTUP_MESSAGE)
        await self.change_presence(status=Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=f"prefix: '{self.__configs.BOT_PREFIX}'"))
        if self.__listingSlash:
            print(self.__messages.STARTUP_COMPLETE_MESSAGE)

    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())

        elif isinstance(error, ExpectedClosingQuoteError):
            await ctx.send("Daan lassen siis bleiben bitte, das ist langsam WIRKLICH nicht mehr witzig mal ehrlich")

        elif isinstance(error, CommandNotFound):
            await ctx.send(embed=self.__embeds.COMMAND_NOT_FOUND())

        elif isinstance(error, UnexpectedQuoteError):
            await ctx.send("Das geht so nicht sie pizzierender spast, machen sie einfach keine quotes")

        elif isinstance(error, BadArgument):
            await ctx.send("Please leave a space between arguments")

        else:
            print(f'Command has thrown an error -> {error}')
            await ctx.send(embed=self.__embeds.UNKNOWN_ERROR())

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
