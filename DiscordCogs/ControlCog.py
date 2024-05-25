from discord import Embed
from discord.ext.commands import Cog, command
from Config.Configs import BConfigs
from Config.Helper import Helper
from Config.Colors import BColors
from Music.BlueshellBot import BlueshellBot
from Config.Embeds import BEmbeds

helper = Helper()


class ControlCog(Cog):
    """Class to handle discord events"""

    def __init__(self, bot: BlueshellBot):
        self.__bot = bot
        self.__config = BConfigs()
        self.__colors = BColors()
        self.__embeds = BEmbeds()
        self.__commands = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop',
                      'skip', 'play', 'queue', 'clear',
                      'np', 'shuffle', 'move', 'remove',
                      'reset', 'prev', 'history', 'volume'],
            'MISC': ['wahl', 'random', 'choose', 'alert', 'clean']
        }

    @command(name="help", help=helper.HELP_HELP, description=helper.HELP_HELP_LONG, aliases=['h'])
    async def help_msg(self, ctx, command_help=''):
        if command_help != '':
            for command in self.__bot.commands:
                if command.name == command_help:
                    txt = command.description if command.description else command.help

                    embedhelp = Embed(
                        title=f'help page for **{command_help}**',
                        description=txt,
                        colour=self.__colors.BLUE
                    )

                    await ctx.send(embed=embedhelp)
                    return

            embedhelp = Embed(
                title='Help',
                description=f'Command "{command_help}" doesn\'t exist, type {self.__config.BOT_PREFIX}help to see all commands',
                colour=self.__colors.BLACK
            )

            await ctx.send(embed=embedhelp)
        else:
            help_music = '🎧 `MUSIC`\n'
            help_misc = '🗿 `MISC`\n'
            help_help = '🥺 `HELP`\n'

            for command in self.__bot.commands:
                if command.name in self.__commands['MUSIC']:
                    help_music += f'**{command}**, '

                elif command.name in self.__commands['MISC']:
                    help_misc += f'**{command}** - {command.help}\n'

                else:
                    help_help += f'**{command}** - {command.help}\n'
            help_music = help_music[:-2] + '\n'

            helptxt = f'\n{help_music}\n{help_help}\n{help_misc}'
            helptxt += f'\n\nType {self.__config.BOT_PREFIX}help <command> for more info'
            embedhelp = Embed(
                title=f'**Commands: {self.__bot.user.name}**',
                description=helptxt,
                colour=self.__colors.BLUE
            )

            if self.__bot.user.avatar != None:
                embedhelp.set_thumbnail(url=self.__bot.user.avatar)
            await ctx.send(embed=embedhelp)

    @command(name='invite', help=helper.HELP_INVITE, description=helper.HELP_INVITE_LONG, aliases=['inv'])
    async def invite_bot(self, ctx):
        invite_url = self.__config.INVITE_URL.format(self.__bot.user.id)
        txt = self.__config.INVITE_MESSAGE.format(invite_url, invite_url)

        embed = Embed(
            title="Invite",
            description=txt,
            colour=self.__colors.BLUE
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ControlCog(bot))
