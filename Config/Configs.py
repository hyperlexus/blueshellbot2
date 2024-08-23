import os
from dotenv import load_dotenv
from Config.Singleton import Singleton
from Config.Folder import Folder

load_dotenv()


class BConfigs(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.BOT_TOKEN = os.getenv('BOT_TOKEN')
            if self.BOT_TOKEN is None:
                raise ValueError('No token was given. You can find your bot token on the Discord Developer Portal')
            self.SPOTIFY_ID = os.getenv('SPOTIFY_ID')
            self.SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
            if self.SPOTIFY_ID == "Your_Own_Spotify_ID" or self.SPOTIFY_SECRET == "Your_Own_Spotify_Secret":
                self.SPOTIFY_ID = None
                self.SPOTIFY_SECRET = None
                print('Spotify will not work.')

            self.BOT_ADMINS = os.getenv('BOT_ADMINS', '')
            self.BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
            if self.BOT_PREFIX == 'Your_Wanted_Prefix_For_Blueshell':
                self.BOT_PREFIX = '!'
            self.BAT_PATH = os.getenv('BAT_PATH', '')
            self.PROJECT_PATH = os.getenv('PROJECT_PATH', '')

            self.SHOULD_AUTO_DISCONNECT_WHEN_ALONE = os.getenv('SHOULD_AUTO_DISCONNECT_WHEN_ALONE') == 'True'
            self.SONG_PLAYBACK_IN_SEPARATE_PROCESS = os.getenv('SONG_PLAYBACK_IN_SEPARATE_PROCESS', 'True') == 'True'
            self.MAX_DOWNLOAD_SONGS_AT_A_TIME = int(os.getenv('MAX_DOWNLOAD_SONGS_AT_A_TIME', 10))
            self.CLEANER_MESSAGES_QUANT = int(os.getenv('CLEANER_MESSAGES_QUANT', 25))
            self.CLEAN_AMOUNT = int(os.getenv('CLEAN_AMOUNT', 100))
            self.ACQUIRE_LOCK_TIMEOUT = int(os.getenv('ACQUIRE_LOCK_TIMEOUT', 10))
            self.QUEUE_VIEW_TIMEOUT = int(os.getenv('QUEUE_VIEW_TIMEOUT', 120))
            self.COMMANDS_FOLDER_NAME = os.getenv('COMMANDS_FOLDER_NAME', 'DiscordCogs')
            self.COMMANDS_PATH = f'{Folder().rootFolder}{self.COMMANDS_FOLDER_NAME}'
            self.VC_TIMEOUT = int(os.getenv('VC_TIMEOUT', 300))
            self.CHANCE_SHOW_TEXT = int(os.getenv('CHANCE_SHOW_TEXT', 1))
            self.MAX_PLAYLIST_LENGTH = int(os.getenv('MAX_PLAYLIST_LENGTH', 50))
            self.MAX_PLAYLIST_FORCED_LENGTH = int(os.getenv('MAX_PLAYLIST_FORCED_LENGTH', 5))
            self.MAX_SONGS_IN_PAGE = int(os.getenv('MAX_SONGS_IN_PAGE', 10))
            self.MAX_PRELOAD_SONGS = int(os.getenv('MAX_PRELOAD_SONGS', 15))
            self.MAX_SONGS_HISTORY = int(os.getenv('MAX_SONGS_HISTORY', 15))
            self.INVITE_MESSAGE = os.getenv('INVITE_MESSAGE', """Invite link: [here]({})""")

            self.MY_ERROR_BAD_COMMAND = os.getenv('MY_ERROR_BAD_COMMAND', 'This string serves to verify if some error was raised by myself on purpose')
            self.INVITE_URL = os.getenv('INVITE_URL', 'https://discord.com/oauth2/authorize?client_id=1242900773659086890&permissions=8&scope=bot')
            self.PROJECT_URL = os.getenv('PROJECT_URL', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            self.SUPPORTING_ICON = os.getenv('SUPPORTING_ICON', 'https://i.ytimg.com/vi/zktTuXl24dk/maxresdefault.jpg')


    def getPlayersManager(self):
        return self.__manager

    def setPlayersManager(self, newManager):
        self.__manager = newManager
