import os
from random import choices
import string
from discord.bot import Bot
from discord import Intents
from Music.BlueshellBot import BlueshellBot
from os import listdir
from Config.Configs import BConfigs
from Config.Exceptions import BlueshellError


class BlueshellInitializer:
    def __init__(self, willListen: bool) -> None:
        self.__config = BConfigs()
        self.__intents = Intents.default()
        self.__intents.message_content = True
        self.__intents.members = True
        self.__bot = self.__create_bot(willListen)
        self.__add_cogs(self.__bot)

    def getBot(self) -> BlueshellBot:
        return self.__bot

    def __create_bot(self, willListen: bool) -> BlueshellBot:
        if willListen:
            prefix = self.__config.BOT_PREFIX
            bot = BlueshellBot(listingSlash=True,
                               command_prefix=prefix,
                               pm_help=True,
                               case_insensitive=True,
                               intents=self.__intents)
        else:
            prefix = ''.join(choices(string.ascii_uppercase + string.digits, k=4))
            bot = BlueshellBot(listingSlash=False,
                               command_prefix=prefix,
                               pm_help=True,
                               case_insensitive=True,
                               intents=self.__intents)
        return bot

    def __add_cogs(self, bot: Bot) -> None:
        try:
            cogsStatus = []

            for root, dirs, files in os.walk(self.__config.COMMANDS_PATH):
                for file in files:
                    if file.endswith('.py'):
                        cogPath = f'{self.__config.COMMANDS_FOLDER_NAME}.{file[:-3]}'
                        cogsStatus.append(bot.load_extension(cogPath, store=True))

            if len(bot.cogs.keys()) != self.__getTotalCogs():
                print(cogsStatus)
                raise BlueshellError(message='Failed to load a Cog')

        except BlueshellError as e:
            print(f'[Error Loading Blueshellbot]')
            print(e)

    def __getTotalCogs(self) -> int:
        quant = 0

        for root, dirs, files in os.walk(self.__config.COMMANDS_PATH):
            for file in files:
                if file.endswith('.py'):
                    quant += 1

        return quant
