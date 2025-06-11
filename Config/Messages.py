from Config.Singleton import Singleton
from Config.Configs import BConfigs
from Config.Emojis import BEmojis


class Messages(Singleton):
    def __init__(self) -> None:


        if not super().created:
            self.__emojis = BEmojis()
            configs = BConfigs()
            self.STARTUP_MESSAGE = 'starting bot'
            self.STARTUP_COMPLETE_MESSAGE = 'bot is running.'
            self.INVITE_URL = 'https://discord.com/oauth2/authorize?client_id=1242900773659086890&permissions=8&scope=bot'
            self.INVITE_MESSAGE = 'Balls, idk this is not needed but if i remove it it breaks lol (dunno why)'

            self.SONGINFO_UPLOADER = "Channel/Artist: "
            self.SONGINFO_DURATION = "Duration: "
            self.SONGINFO_REQUESTER = 'Requested by: '
            self.SONGINFO_POSITION = 'Position in Queue: '
            self.SONGINFO_UNKNOWN_DURATION = 'Unknown duration.'

            self.VOLUME_CHANGED = 'Volume changed to `{}`%'
            self.SONGS_ADDED = 'Downloading `{}` songs.'
            self.SONG_ADDED = 'Downloading `{}`'
            self.SONG_ADDED_TWO = f'{self.__emojis.MUSIC} Song added to queue'
            self.SONG_PLAYING = f'Now Playing'
            self.SONG_PLAYER = f'Song Player'
            self.QUEUE_TITLE = f'Queue'
            self.ONE_SONG_LOOPING = f'{self.__emojis.MUSIC} Looping One Song'
            self.ALL_SONGS_LOOPING = f'{self.__emojis.MUSIC} Looping All Songs'
            self.SONG_PAUSED = f'{self.__emojis.PAUSE} Song paused'
            self.SONG_RESUMED = f'{self.__emojis.PLAY} Song playing'
            self.SONG_SKIPPED = f'{self.__emojis.SKIP} Song skipped'
            self.RETURNING_SONG = f'{self.__emojis.BACK} Playing previous song'
            self.STOPPING = f'{self.__emojis.LEAVE} You made ~~this instance of~~ me kill myself. Statement?'
            self.EMPTY_QUEUE = f'{self.__emojis.QUEUE} Queue is empty.'
            self.SONG_DOWNLOADING = f'{self.__emojis.DOWNLOADING} Downloading...'
            self.PLAYLIST_CLEAR = f'{self.__emojis.MUSIC} Playlist is now empty'

            self.HISTORY_TITLE = f'{self.__emojis.MUSIC} Played Songs'
            self.HISTORY_EMPTY = f'{self.__emojis.QUEUE} History is empty. Pay attention next time.'

            self.SONG_MOVED_SUCCESSFULLY = 'Song `{}` in position `{}` moved to position `{}`.'
            self.SONG_REMOVED_SUCCESSFULLY = 'Song `{}` removed successfully'

            self.LOOP_ALL_ON = f'{self.__emojis.ERROR} Loop already set to "all", use {configs.BOT_PREFIX}loop off to disable the loop first'
            self.LOOP_ONE_ON = f'{self.__emojis.ERROR} Loop already set to "one", use {configs.BOT_PREFIX}loop off to disable this loop first'
            self.LOOP_ALL_ALREADY_ON = f'{self.__emojis.LOOP_ALL} "Loop all" is already the current loop state.'
            self.LOOP_ONE_ALREADY_ON = f'{self.__emojis.LOOP_ONE} "Loop one" is already the current loop state.'
            self.LOOP_ALL_ACTIVATE = f'{self.__emojis.LOOP_ALL} Looping all songs'
            self.LOOP_ONE_ACTIVATE = f'{self.__emojis.LOOP_ONE} Looping the current song'
            self.LOOP_DISABLE = f'{self.__emojis.LOOP_OFF} Loop disabled'
            self.LOOP_ALREADY_DISABLE = f'{self.__emojis.ERROR} Loop is already off.'
            self.LOOP_ON = f'{self.__emojis.ERROR} Loop is already on.'
            self.BAD_USE_OF_LOOP = (f"{self.__emojis.ERROR} You can't use 'loop' like this. Check {configs.BOT_PREFIX}help loop"
                                    f"-> Possible commands: all, off, one, ''")

            self.SONGS_SHUFFLED = f'{self.__emojis.SHUFFLE} Shuffled.'
            self.ERROR_SHUFFLING = f'{self.__emojis.ERROR} Shuffle not on. No clue why tho.'
            self.ERROR_MOVING = f'{self.__emojis.ERROR} That move didnt work. unfortunately idk why, maybe you used the command wrong dumbass'
            self.LENGTH_ERROR = f'{self.__emojis.ERROR} Numbers must be between 1 and queue length, use -1 for the last song'
            self.ERROR_NUMBER = f'{self.__emojis.ERROR} This command requires a number'
            self.ERROR_VOLUME_NUMBER = f'{self.__emojis.ERROR} Volume is in %. Why would you specify anything outside (0,100)?'
            self.ERROR_VOLUME_NOT_SPECIFIED = f'{self.__emojis.ERROR} Please pass an argument to the volume function. Its bit unintuitive sorry xd'
            self.ERROR_PLAYING = f'{self.__emojis.ERROR} song couldnt play for some reason'
            self.COMMAND_NOT_FOUND = f'{self.__emojis.ERROR} That command doesnt exist. Run {configs.BOT_PREFIX}help for a list'
            self.UNKNOWN_ERROR = f'{self.__emojis.ERROR} something failed lul.'
            self.ERROR_MISSING_ARGUMENTS = f'{self.__emojis.ERROR} You\'re missing some arguments there. Check help page for the command'
            self.NOT_PREVIOUS = f'{self.__emojis.ERROR} This is the first song you played.'
            self.PLAYER_NOT_PLAYING = f'{self.__emojis.ERROR} The player isnt even playing'
            self.IMPOSSIBLE_MOVE = 'IMPOSSIBLE TRAIN'
            self.ERROR_TITLE = 'Error. Unfortunate'
            self.COMMAND_NOT_FOUND_TITLE = 'Command doesnt exist'
            self.NO_CHANNEL = 'You arent in a vc.'
            self.NO_GUILD = f'Something weird is going on, the server apparently has "no guild", try {configs.BOT_PREFIX}reset'
            self.INVALID_INPUT = f'Invalid input. try {configs.BOT_PREFIX}help play'
            self.INVALID_INDEX = f'Invalid index passed as argument.'
            self.INVALID_ARGUMENTS = f'Invalid arguments passed to command.'
            self.DOWNLOADING_ERROR = f"{self.__emojis.ERROR} This didn't download. Unlucky."
            self.EXTRACTING_ERROR = f'{self.__emojis.ERROR} Couldn\'t search for songs. Failed while extracting'

            self.ERROR_IN_PROCESS = f"{self.__emojis.ERROR} internal error, player was restarted, song was skipped. 😂🫵"
            self.MY_ERROR_BAD_COMMAND = 'just here for testing.'
            self.BAD_COMMAND_TITLE = 'You can\'t use that that way.'
            self.BAD_COMMAND = f'{self.__emojis.ERROR} Bad usage of this command.'
            self.VIDEO_UNAVAILABLE = f'{self.__emojis.ERROR} Video unavailable.'
            self.ERROR_DUE_LOOP_ONE_ON = f'{self.__emojis.ERROR} "Loop 1" is on, making this impossible. Try again with loop set to all or off.'

            self.BAD_ABSOLUTE_ALERT = f'{self.__emojis.ERROR} Use {configs.BOT_PREFIX}alert thh:mm'


class SearchMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.UNKNOWN_INPUT = 'Unknown Provider (not plaintext, not youtube, spotify or deezer).'
            self.UNKNOWN_INPUT_TITLE = 'Nothing Found'
            self.GENERIC_TITLE = 'URL didnt work.'
            self.SPOTIFY_NOT_FOUND = 'Spotify didn\'t find any songs.'
            self.YOUTUBE_NOT_FOUND = 'Youtube didn\'t find any songs.'
            self.DEEZER_NOT_FOUND = 'Couldn\'t find Deezer. As the Germans would say, kein WLAN, kein WLAN; Zeezer.'


class SpotifyMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.INVALID_SPOTIFY_URL = 'Invalid Spotify URL, verify your link.'
            self.GENERIC_TITLE = 'URL could not be processed'


class DeezerMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.INVALID_DEEZER_URL = 'Invalid Deezer URL, verify your link.'
            self.GENERIC_TITLE = 'URL could not be processed'
