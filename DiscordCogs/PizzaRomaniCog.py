import json
from Music.BlueshellBot import BlueshellBot
from discord.ext.commands import Context, command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs

helper = Helper()

global is_pizza_on
# all_pizza_commands = []
with open("pizza_database.json", "r") as f:
    data = json.load(f)
    all_pizza_commands = data['commands']


class PizzaRomaniCog(Cog):
    """ich ess pizza"""
    def __init__(self, bot: BlueshellBot):
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.__bot: BlueshellBot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.__bot.user:
            return

        if not message.content:
            return

        for count, current_dict in enumerate(all_pizza_commands):
            send = False
            if current_dict['read'] in message.content.lower():
                if current_dict['type'] == 'in':
                    send = True

                elif current_dict['type'] == 'is':
                    if message.content == current_dict['read']:
                        send = True

                elif current_dict['type'] == 'start':
                    if message.content.startswith(current_dict['read']):
                        send = True

                elif current_dict['type'] == 'end':
                    print(current_dict['read'])
                    if message.content.endswith(current_dict['read']):
                        send = True

            if send:
                await message.channel.send(current_dict['write'])

    @command(name='pinsert', help=helper.HELP_PINSERT, description=helper.HELP_PINSERT_LONG)
    async def pinsert(self, ctx: Context, *args):
        if len(args) != 3:
            embed = self.__embeds.BAD_COMMAND_USAGE("pizza_insert")
            await ctx.send(embed)
            return



        await ctx.send(', '.join(args))
        return


def setup(bot):
    bot.add_cog(PizzaRomaniCog(bot))
