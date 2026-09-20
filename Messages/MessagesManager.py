from typing import Dict, List
from Config.Singleton import Singleton
from UI.Views.AbstractView import AbstractView
from Messages.MessagesCategory import MessagesCategory
from Messages.DiscordMessages import BAbstractMessage
import traceback


class MessagesManager(Singleton):
    def __init__(self) -> None:
        if not super().created:
            # make a list of messages for every guild and category
            self.__guild_messages: dict[int, dict[MessagesCategory, list[BAbstractMessage]]] = {}
            # will, for each message, store the AbstractView that controls it
            self.__messagesViews: dict[BAbstractMessage, AbstractView] = {}

    def addMessage(self, guild_id: int, category: MessagesCategory, message: BAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # create dict if guild doesnt exist
        if guild_id not in self.__guild_messages.keys():
            self.__guild_messages[guild_id] = {}
        # add category if not in guild
        if category not in self.__guild_messages[guild_id].keys():
            self.__guild_messages[guild_id][category] = []

        sent_messages = self.__guild_messages[guild_id][category]
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view
        sent_messages.append(message)

    async def addMessageAndClearPrevious(self, guild_id: int, category: MessagesCategory, message: BAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # If guild doesn't exist, create Dict
        if guild_id not in self.__guild_messages.keys():
            self.__guild_messages[guild_id] = {}
        # add category if it's not in guild
        if category not in self.__guild_messages[guild_id].keys():
            self.__guild_messages[guild_id][category] = []

        sent_messages = self.__guild_messages[guild_id][category]

        # delete all sent messages in the category
        for previousMessage in sent_messages:
            await self.__deleteMessage(previousMessage)

        # Create a new list with only the new message
        self.__guild_messages[guild_id][category] = [message]

        # Store the view of this message
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view

    async def clearMessagesOfCategory(self, guild_id: int, category: MessagesCategory) -> None:
        sent_messages = self.__guild_messages[guild_id][category]

        for message in sent_messages:
            await self.__deleteMessage(message)

    async def clearMessagesOfGuild(self, guild_id: int) -> None:
        category_messages = self.__guild_messages[guild_id]

        for category in category_messages.keys():
            for message in category_messages[category]:
                await self.__deleteMessage(message)

    async def __deleteMessage(self, message: BAbstractMessage) -> None:
        try:
            # If there is a view for this message delete the key
            if message in self.__messagesViews.keys():
                message_view = self.__messagesViews.pop(message)
                message_view.stopView()
                del message_view

            await message.delete()
        except:
            pass
            # print(message.__str__())
            # print(f'[ERROR DELETING MESSAGE] -> {traceback.format_exc()}')
