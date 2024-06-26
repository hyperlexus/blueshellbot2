from Messages.Responses.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Messages.DiscordMessages import BAbstractMessage, BDefaultMessage


class EmbedCommandResponse(AbstractCommandResponse):
    def __init__(self, response: HandlerResponse, category: MessagesCategory) -> None:
        super().__init__(response, category)

    async def run(self, deleteLast: bool = True) -> None:
        message = None
        # If the response has both embed and view to be sent
        if self.response.embed and self.response.view:
            message = await self.context.send(embed=self.response.embed, view=self.response.view)
            # Set the view to contain the sent message
            self.response.view.set_message(message)

        # Or just a embed
        elif self.response.embed:
            message = await self.context.send(embed=self.response.embed, delete_after=5)

        if message:
            vMessage: BAbstractMessage = BDefaultMessage(message)
            # Only delete the previous message if there's no error and isn't forbidden by method caller
            if deleteLast and self.response.success:
                await self.manager.addMessageAndClearPrevious(self.context.guild.id, self.category, vMessage, self.response.view)
            else:
                self.manager.addMessage(self.context.guild.id, self.category, vMessage)
