import asyncio
import traceback
from typing import List, Union
from Config.Exceptions import DownloadingError, InvalidInput, BlueshellError
from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import ImpossibleTrain, UnknownError
from Handlers.HandlerResponse import HandlerResponse
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Music.Song import Song
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Parallelism.Commands import BCommands, BCommandsType
from Music.BlueshellBot import BlueshellBot
from discord import Interaction


class PlayHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: BlueshellBot) -> None:
        super().__init__(ctx, bot)
        self.__searcher = Searcher()
        self.__down = Downloader()

    async def run(self, track: str) -> HandlerResponse:
        requester = self.ctx.author.name

        if not self.__isUserConnected():
            error = ImpossibleTrain()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)
        try:
            # Search for songs and get the name of each song
            songsInfo = await self.__searcher.search(track)
            if songsInfo is None or len(songsInfo) == 0:
                raise InvalidInput(self.messages.INVALID_INPUT, self.messages.ERROR_TITLE)

            # If there is no executing player for the guild then we create the player
            playersManager: AbstractPlayersManager = self.config.getPlayersManager()
            if not playersManager.verifyIfPlayerExists(self.guild):
                playersManager.createPlayerForGuild(self.guild, self.ctx)

            playlist = playersManager.getPlayerPlaylist(self.guild)

            # Create the Songs objects
            songs: List[Song] = []
            for musicInfo in songsInfo:
                songs.append(Song(musicInfo, playlist, requester))

            if len(songs) == 1:
                # If only one song, download it directly
                song = self.__down.finish_one_song(songs[0])
                if song.problematic:  # If error in download song return
                    embed = self.embeds.SONG_PROBLEMATIC()
                    error = DownloadingError()
                    return HandlerResponse(self.ctx, embed, error)

                # If not playing
                if not playlist.getCurrentSong():
                    embed = self.embeds.SONG_ADDED(song.title)
                    response = HandlerResponse(self.ctx, embed)
                else:  # If already playing
                    pos = len(playlist.getSongs())
                    embed = self.embeds.SONG_ADDED_TWO(song.info, pos)
                    response = HandlerResponse(self.ctx, embed)

                # Add the unique song to the playlist and send a command to player
                playerLock = playersManager.getPlayerLock(self.guild)
                acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
                if acquired:
                    playlist.add_song(song)
                    # Release the acquired Lock
                    playerLock.release()
                    playCommand = BCommands(BCommandsType.PLAY, None)
                    await playersManager.sendCommandToPlayer(playCommand, self.guild, self.ctx)
                else:
                    playersManager.resetPlayer(self.guild, self.ctx)
                    embed = self.embeds.PLAYER_RESTARTED()
                    return HandlerResponse(self.ctx, embed)

                return response
            else:  # If multiple songs added
                # Trigger a task to download all songs and then store them in the playlist
                asyncio.create_task(self.__downloadSongsInBatches(songs, playersManager))

                embed = self.embeds.SONGS_ADDED(len(songs))
                return HandlerResponse(self.ctx, embed)

        except DownloadingError as error:
            embed = self.embeds.DOWNLOADING_ERROR()
            return HandlerResponse(self.ctx, embed, error)
        except Exception as error:
            print(f'[ERROR IN PLAYHANDLER] -> {traceback.format_exc()}', {type(error)})
            if isinstance(error, BlueshellError):
                embed = self.embeds.CUSTOM_ERROR(error)
            else:
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()

            return HandlerResponse(self.ctx, embed, error)

    async def __downloadSongsInBatches(self, songs: List[Song], playersManager: AbstractPlayersManager) -> None:
        playlist = playersManager.getPlayerPlaylist(self.guild)
        playCommand = BCommands(BCommandsType.PLAY, None)
        maxDownloads = self.config.MAX_DOWNLOAD_SONGS_AT_A_TIME

        while len(songs) > 0:
            # Verify how many songs will be downloaded in this batch and extract from the songs list
            songsQuant = min(maxDownloads, len(songs))
            # Get the first quantInBatch songs
            songsInBatch = songs[:songsQuant]
            # Remove the first quantInBatch songs from the songs
            songs = songs[songsQuant:]

            # Create task to download the songs in the batch
            tasks: List[asyncio.Task] = []
            for index, song in enumerate(songsInBatch):
                task = asyncio.create_task(self.__down.download_song(song))
                tasks.append(task)

            for index, task, in enumerate(tasks):
                await task
                song = songsInBatch[index]
                if not song.problematic:  # If downloaded add to the playlist and send play command
                    playerLock = playersManager.getPlayerLock(self.guild)
                    acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
                    if acquired:
                        playlist.add_song(song)
                        await playersManager.sendCommandToPlayer(playCommand, self.guild, self.ctx)
                        playerLock.release()
                    else:
                        playersManager.resetPlayer(self.guild, self.ctx)

    def __isUserConnected(self) -> bool:
        return self.ctx.author.voice
