from Messages.Responses.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Messages.DiscordMessages import BAbstractMessage, BWebHookMessage
from discord import ApplicationContext


class SlashEmbedResponse(AbstractCommandResponse):
    def __init__(self, response: HandlerResponse, ctx: ApplicationContext, category: MessagesCategory) -> None:
        self.__ctx = ctx
        super().__init__(response, category)

    async def run(self, deleteLast: bool = True) -> None:
        message = None
        # If the response has both embed and view to send
        if self.response.embed and self.response.view:
            # Respond to the Slash command and set the view to contain the sent message
            message = await self.__ctx.send_followup(embed=self.response.embed, view=self.response.view)
            self.response.view.set_message(message)

        # If the response only has the embed then send the embed
        elif self.response.embed:
            message = await self.__ctx.send_followup(embed=self.response.embed)
        else:
            message = await self.__ctx.send_followup('Ok!')

        # If any message was sended
        if message:
            # Convert the Discord message type to a Blueshell type
            vMessage: BAbstractMessage = BWebHookMessage(message)
            # Only delete the previous message if this is not error and not forbidden by method caller
            if deleteLast and self.response.success:
                await self.manager.addMessageAndClearPrevious(self.context.guild.id, self.category, vMessage, self.response.view)
            else:
                self.manager.addMessage(self.context.guild.id, self.category, vMessage)
