from discord import Message, WebhookMessage
from abc import ABC, abstractmethod


class BAbstractMessage(ABC):
    """
    Abstract class to allow create a pattern when dealing with multiple Discord
    messages types, such as Interaction Messages and the standard discord messages
    that contains two different ways of deletion 
    """
    @abstractmethod
    async def delete(self):
        pass


class BWebHookMessage(BAbstractMessage):
    """
    Holds a WebhookMessage instance 
    """

    def __init__(self, message: WebhookMessage) -> None:
        self.__message = message
        super().__init__()

    async def delete(self):
        await self.__message.delete()


class BDefaultMessage(BAbstractMessage):
    """
    Holds a Message instance, the basic Discord message type
    """

    def __init__(self, message: Message) -> None:
        self.__message = message
        super().__init__()

    async def delete(self):
        await self.__message.delete()
