import asyncio
import traceback
from asyncio import AbstractEventLoop
from datetime import datetime
import discord
from discord import Guild, Status, Game, Message
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, ExpectedClosingQuoteError, \
    UnexpectedQuoteError, BadArgument, InvalidEndOfQuotedStringError, CheckFailure
from Config.Configs import BConfigs
from Config.Messages import Messages
from Config.Embeds import BEmbeds
from Utils.Utils import Utils

blueshell_entire_bot_startup_timestamp = datetime.now()

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
        actual_error = getattr(error, 'original', error)
        if isinstance(actual_error, MissingRequiredArgument):
            await ctx.send(embed=self.__embeds.MISSING_ARGUMENTS())

        elif isinstance(actual_error, ExpectedClosingQuoteError):
            await ctx.send(embed=self.__embeds.NO_CLOSING_QUOTE())

        elif isinstance(actual_error, CommandNotFound):
            await ctx.send(embed=self.__embeds.COMMAND_NOT_FOUND())

        elif isinstance(actual_error, InvalidEndOfQuotedStringError):
            await ctx.send("Please leave a space between arguments")

        elif isinstance(actual_error, UnexpectedQuoteError):
            await ctx.send("Das geht so nicht sie pizzierender spast, machen sie einfach keine quotes")

        elif isinstance(actual_error, CheckFailure):
            return

        else:
            tb = traceback.extract_tb(actual_error.__traceback__)
            if tb:
                last_frame = tb[-1]
                file_name = last_frame.filename.split("/")[-1]
                line_no = last_frame.lineno
                location_info = f"in {file_name}:{line_no}"
            else:
                location_info = "unknown location"

            error_type = type(actual_error).__name__
            print(f"Unhandled error: {error_type} at {location_info}")
            print(f'Command has thrown an error -> {actual_error}')
            await ctx.send(embed=self.__embeds.UNKNOWN_ERROR(f"{error_type} ({location_info})"))

    async def on_application_command_error(self, ctx, error):
        actual_error = getattr(error, 'original', error)
        if isinstance(error, CheckFailure) or isinstance(actual_error, CheckFailure):
            return

        else:
            tb = traceback.extract_tb(actual_error.__traceback__)
            if tb:
                last_frame = tb[-1]
                file_name = last_frame.filename.split("/")[-1]
                line_no = last_frame.lineno
                location_info = f"in {file_name}:{line_no}"
            else:
                location_info = "unknown location"

            error_type = type(actual_error).__name__
            print(f"Unhandled error: {error_type} at {location_info}")
            print(f'Slash command has thrown an error -> {actual_error}')
            await ctx.respond(embed=self.__embeds.UNKNOWN_SLASH_COMMAND_ERROR(f"{error_type} ({location_info})"))

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
