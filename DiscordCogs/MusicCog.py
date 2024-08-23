import os
from discord.ext.commands import Context, command, Cog
from Config.Exceptions import InvalidInput
from Config.Helper import Helper
from Handlers.ClearHandler import ClearHandler
from Handlers.HandlerResponse import HandlerResponse
from Handlers.MoveHandler import MoveHandler
from Handlers.NowPlayingHandler import NowPlayingHandler
from Handlers.PlayHandler import PlayHandler
from Handlers.PrevHandler import PrevHandler
from Handlers.RemoveHandler import RemoveHandler
from Handlers.ResetHandler import ResetHandler
from Handlers.ShuffleHandler import ShuffleHandler
from Handlers.SkipHandler import SkipHandler
from Handlers.PauseHandler import PauseHandler
from Handlers.StopHandler import StopHandler
from Handlers.ResumeHandler import ResumeHandler
from Handlers.HistoryHandler import HistoryHandler
from Handlers.QueueHandler import QueueHandler
from Handlers.LoopHandler import LoopHandler
from Handlers.VolumeHandler import VolumeHandler
from Messages.MessagesCategory import MessagesCategory
from Messages.Responses.EmoteCogResponse import EmoteCommandResponse
from Messages.Responses.EmbedCogResponse import EmbedCommandResponse
from Music.BlueshellBot import BlueshellBot
from Config.Configs import BConfigs
from Config.Embeds import BEmbeds
from Parallelism.ProcessPlayerManager import ProcessPlayerManager
from Parallelism.ThreadPlayerManager import ThreadPlayerManager

helper = Helper()
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def check_bans(path) -> list:
    banned_ids = []
    os.chdir(path)
    with open("./banlist.txt", "r") as file:
        for line in file:
            try:
                banned_ids.append(int(line))
            except ValueError:
                print("something went past the checker in the ban command, and a character is in here")
                return
        return banned_ids

def check_if_banned(user, path) -> bool:
    return True if user in check_bans(path) else False


class MusicCog(Cog):
    """
    Class to listen to Music commands
    It'll listen for commands from discord, when triggered will create a specific Handler for the command
    Execute the handler and then create a specific View to be showed in Discord
    """

    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__config = BConfigs()
        if self.__config.SONG_PLAYBACK_IN_SEPARATE_PROCESS:
            self.__config.setPlayersManager(ProcessPlayerManager(bot))
        else:
            self.__config.setPlayersManager(ThreadPlayerManager(bot))

    @command(name="play", help=helper.HELP_PLAY, description=helper.HELP_PLAY_LONG, aliases=['p', 'paly'])
    async def play(self, ctx: Context, *args) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = PlayHandler(ctx, self.__bot)

            if len(args) > 1:
                track = " ".join(args)
            else:
                track = args[0]

            response = await controller.run(track)
            if response is not None:
                cogResponder1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponder2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponder1.run()
                await cogResponder2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="volume", help=helper.CHANGE_VOLUME, description=helper.CHANGE_VOLUME_LONG, aliases=['v'])
    async def volume(self, ctx: Context, *args) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = VolumeHandler(ctx, self.__bot)

            if len(args) > 1:
                track = " ".join(args)
            elif len(args) == 1:
                track = args[0]
            else:
                track: str = '100'

            response = await controller.run(track)
            if response is not None:
                cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponser1.run()
                await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="queue", help=helper.HELP_QUEUE, description=helper.HELP_QUEUE_LONG, aliases=['q'])
    async def queue(self, ctx: Context, *args) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            pageNumber = " ".join(args)

            controller = QueueHandler(ctx, self.__bot)

            if pageNumber == "":
                response = await controller.run()
            else:
                pageNumber = int(pageNumber)
                pageNumber -= 1  # Change index 1 to 0
                response = await controller.run(pageNumber)

            cogResponser = EmbedCommandResponse(response, MessagesCategory.QUEUE)
            await cogResponser.run()
        except ValueError as e:
            # Draft a Handler Response to pass to cogResponser
            error = InvalidInput()
            embed = self.__embeds.INVALID_ARGUMENTS()
            response = HandlerResponse(ctx, embed, error)

            cogResponser = EmbedCommandResponse(response, MessagesCategory.QUEUE)
            await cogResponser.run(deleteLast=False)
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="skip", help=helper.HELP_SKIP, description=helper.HELP_SKIP_LONG, aliases=['s', 'next'])
    async def skip(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = SkipHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='stop', help=helper.HELP_STOP, description=helper.HELP_STOP_LONG, aliases=['kys', 'leave', 'youshouldkillyourselfnow⚡'])
    async def stop(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = StopHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='pause', help=helper.HELP_PAUSE, description=helper.HELP_PAUSE_LONG, aliases=['pautism'])
    async def pause(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = PauseHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='resume', help=helper.HELP_RESUME, description=helper.HELP_RESUME_LONG, aliases=['unpause'])
    async def resume(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = ResumeHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='prev', help=helper.HELP_PREV, description=helper.HELP_PREV_LONG, aliases=['return', 'previous', 'back'])
    async def prev(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = PrevHandler(ctx, self.__bot)

            response = await controller.run()
            if response is not None:
                cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponser1.run()
                await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='history', help=helper.HELP_HISTORY, description=helper.HELP_HISTORY_LONG, aliases=['previoussongs'])
    async def history(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = HistoryHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.HISTORY)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.HISTORY)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='loop', help=helper.HELP_LOOP, description=helper.HELP_LOOP_LONG, aliases=['l', 'repeat'])
    async def loop(self, ctx: Context, args='') -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = LoopHandler(ctx, self.__bot)

            response = await controller.run(args)
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.LOOP)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.LOOP)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='clear', help=helper.HELP_CLEAR, description=helper.HELP_CLEAR_LONG, aliases=['c', 'clearqueue', 'cq'])
    async def clear(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = ClearHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='np', help=helper.HELP_NP, description=helper.HELP_NP_LONG, aliases=['playing', 'now', 'this', 'nowplaying'])
    async def now_playing(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = NowPlayingHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.NOW_PLAYING)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.NOW_PLAYING)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='shuffle', help=helper.HELP_SHUFFLE, description=helper.HELP_SHUFFLE_LONG, aliases=['randomise'])
    async def shuffle(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = ShuffleHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='move', help=helper.HELP_MOVE, description=helper.HELP_MOVE_LONG, aliases=['mv'])
    async def move(self, ctx: Context, pos1, pos2='1') -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = MoveHandler(ctx, self.__bot)

            response = await controller.run(pos1, pos2)
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='remove', help=helper.HELP_REMOVE, description=helper.HELP_REMOVE_LONG, aliases=['delete'])
    async def remove(self, ctx: Context, position) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = RemoveHandler(ctx, self.__bot)

            response = await controller.run(position)
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='reset', help=helper.HELP_RESET, description=helper.HELP_RESET_LONG, aliases=['restart, fix'])
    async def reset(self, ctx: Context) -> None:
        if check_if_banned(ctx.message.author.id, self.__config.PROJECT_PATH):
            await ctx.send(embed=self.__embeds.BANNED())
            return
        try:
            controller = ResetHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')


def setup(bot):
    bot.add_cog(MusicCog(bot))
