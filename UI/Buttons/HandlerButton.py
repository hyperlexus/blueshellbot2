from discord import ButtonStyle, Interaction, Message, TextChannel
from discord.ui import Button, View

from Config.Emojis import BEmojis
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Messages.MessagesManager import MessagesManager
from Music.BlueshellBot import BlueshellBot


class HandlerButton(Button):
    """Button that will create and execute a Handler Object when clicked"""

    def __init__(self, bot: BlueshellBot, handler: type[AbstractHandler], emoji: BEmojis, textChannel: TextChannel,
                 guildID: int, category: MessagesCategory, label=None, *args, **kwargs):
        super().__init__(label=label, style=ButtonStyle.secondary, emoji=emoji)
        self.__messagesManager = MessagesManager()
        self.__category = category
        self.__guildID = guildID
        self.__channel = textChannel
        self.__bot = bot
        self.__args = args
        self.__kwargs = kwargs
        self.__handlerClass = handler
        self.__view: View = None

    async def callback(self, interaction: Interaction) -> None:
        """Callback to when Button is clicked"""
        # Return to Discord that this command is being processed
        await interaction.response.defer()

        # Create the handler object
        handler = self.__handlerClass(interaction, self.__bot)
        response: HandlerResponse = await handler.run(*self.__args, **self.__kwargs)

        message = None
        if response and response.view is not None:
            message: Message = await self.__channel.send(embed=response.embed, view=response.view)
            response.view.set_message(message)
        elif response.embed:
            message: Message = await self.__channel.send(embed=response.embed)

        # Clear the last category sended message and add the new one
        if message:
            await self.__messagesManager.addMessageAndClearPrevious(self.__guildID, self.__category, message,
                                                                    response.view)

    def set_view(self, view: View):
        self.__view = view

    def get_view(self) -> View:
        return self.__view
