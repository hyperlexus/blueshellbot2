from discord import Embed
from discord.ext.commands import Cog, command
from Config.Configs import BConfigs
from Config.Helper import Helper
from Config.Colors import BColors
from Music.BlueshellBot import BlueshellBot
from Config.Embeds import BEmbeds
from Utils.Utils import Utils

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
            'MOD': ['restart', 'ban', 'force_embed'],
            'JP': ['convkana', 'kanagame'],
            'PIZZA': ['pinsert', 'plist', 'premove', 'pinfo', 'ptestcompiler']
        }

    @command(name="help", help=helper.HELP_HELP, description=helper.HELP_HELP_LONG, aliases=['h', 'hjälp'])
    async def help_msg(self, ctx, command_help=''):
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        if command_help != '':
            for assigned_command in self.__bot.commands:
                if assigned_command.name == command_help:
                    txt = assigned_command.description if assigned_command.description else assigned_command.help

                    embedhelp = Embed(
                        title=f'help page for `{self.__config.BOT_PREFIX}{command_help}`',
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
            help_mod = '🎩 `MOD`\n'
            help_jp = '🇯🇵 `JP`\n'
            help_pizza = '🍕 `PIZZA`\n'

            for cmd in self.__bot.commands:
                if cmd.name in self.__commands['MUSIC']:
                    help_music += f'**{cmd}**, '

                elif cmd.name in self.__commands['MOD']:
                    help_mod += f'**{cmd}** - {cmd.help}\n'

                elif cmd.name in self.__commands['JP']:
                    help_jp += f'**{cmd}** - {cmd.help}\n'

                elif cmd.name in self.__commands['PIZZA']:
                    help_pizza += f'**{cmd}** - {cmd.help}\n'

                else:
                    help_misc += f'**{cmd}** - {cmd.help}\n'
            help_music = help_music[:-2] + '\n'

            helptxt = f'\n{help_music}\n{help_misc}\n{help_jp}\n{help_pizza}\n{help_mod}'
            helptxt += f'\n\nType {self.__config.BOT_PREFIX}help <cmd> for more info'
            embedhelp = Embed(
                title=f'**Commands: {self.__bot.user.name}**',
                description=helptxt,
                colour=self.__colors.BLUE
            )

            if self.__bot.user.avatar is None:
                embedhelp.set_thumbnail(url=self.__bot.user.avatar)
            await ctx.send(embed=embedhelp)

    @command(name='invite', help=helper.HELP_INVITE, description=helper.HELP_INVITE_LONG, aliases=['inv'])
    async def invite_bot(self, ctx):
        if Utils.check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
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
