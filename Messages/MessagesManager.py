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
            self.__guildsMessages: Dict[int, Dict[MessagesCategory, List[BAbstractMessage]]] = {}
            # will, for each message, store the AbstractView that controls it
            self.__messagesViews: Dict[BAbstractMessage, AbstractView] = {}

    def addMessage(self, guildID: int, category: MessagesCategory, message: BAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # create dict if guild doesnt exist
        if guildID not in self.__guildsMessages.keys():
            self.__guildsMessages[guildID] = {}
        # add category if not in guild
        if category not in self.__guildsMessages[guildID].keys():
            self.__guildsMessages[guildID][category] = []

        sendedMessages = self.__guildsMessages[guildID][category]
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view
        sendedMessages.append(message)

    async def addMessageAndClearPrevious(self, guildID: int, category: MessagesCategory, message: BAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # If guild doesn't exist, create Dict
        if guildID not in self.__guildsMessages.keys():
            self.__guildsMessages[guildID] = {}
        # add category if it's not in guild
        if category not in self.__guildsMessages[guildID].keys():
            self.__guildsMessages[guildID][category] = []

        sentMessages = self.__guildsMessages[guildID][category]

        # delete all sent messages in the category
        for previousMessage in sentMessages:
            await self.__deleteMessage(previousMessage)

        # Create a new list with only the new message
        self.__guildsMessages[guildID][category] = [message]

        # Store the view of this message
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view

    async def clearMessagesOfCategory(self, guildID: int, category: MessagesCategory) -> None:
        sentMessages = self.__guildsMessages[guildID][category]

        for message in sentMessages:
            self.__deleteMessage(message)

    async def clearMessagesOfGuild(self, guildID: int) -> None:
        categoriesMessages = self.__guildsMessages[guildID]

        for category in categoriesMessages.keys():
            for message in categoriesMessages[category]:
                self.__deleteMessage(message)

    async def __deleteMessage(self, message: BAbstractMessage) -> None:
        try:
            # If there is a view for this message delete the key
            if message in self.__messagesViews.keys():
                messageView = self.__messagesViews.pop(message)
                messageView.stopView()
                del messageView

            await message.delete()
        except Exception:
            print(f'[ERROR DELETING MESSAGE] -> {traceback.format_exc()}')
