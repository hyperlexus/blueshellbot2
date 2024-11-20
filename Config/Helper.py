from Config.Singleton import Singleton
from Config.Configs import BConfigs


class Helper(Singleton):
    def __init__(self) -> None:
        if not super().created:
            config = BConfigs()
            self.HELP_SKIP = 'skip skip skip a beat'
            self.HELP_SKIP_LONG = 'Skips current song. Won\'t work if "loop one" is on'
            self.HELP_RESUME = 'Resumes the song player.'
            self.HELP_RESUME_LONG = 'Resume if paused'
            self.HELP_CLEAR = 'Clear the queue and songs history.'
            self.HELP_CLEAR_LONG = 'Clear queue and history'
            self.HELP_STOP = 'Make the bot kill itself.'
            self.HELP_STOP_LONG = 'Make the bot kill itself.'
            self.HELP_LOOP = 'Loop functionality'
            self.HELP_LOOP_LONG = 'Loop functionality.\nArgs: one, off, all, ""'
            self.HELP_NP = 'Show the info of the current song.'
            self.HELP_NP_LONG = 'Show "Now Playing"'
            self.HELP_QUEUE = f'Show the first {config.MAX_SONGS_IN_PAGE} songs in queue.'
            self.HELP_QUEUE_LONG = f'Show the first {config.MAX_SONGS_IN_PAGE} songs in the queue.'
            self.HELP_PAUSE = 'Pauses the song player.'
            self.HELP_PAUSE_LONG = 'Pauses.'
            self.HELP_PREV = 'Play the previous song.'
            self.HELP_PREV_LONG = 'Plays previous song. If a song is playing, it will return to the previous song.'
            self.HELP_SHUFFLE = 'Shuffle the songs playing.'
            self.HELP_SHUFFLE_LONG = 'Shuffles.'
            self.HELP_PLAY = 'Plays a song.'
            self.CHANGE_VOLUME = 'Set volume'
            self.CHANGE_VOLUME_LONG = 'Set volume between 0 and 100.'
            self.HELP_PLAY_LONG = 'Plays a song.'
            self.HELP_HISTORY = f'Show song history.'
            self.HELP_HISTORY_LONG = f'Show the last {config.MAX_SONGS_HISTORY} played songs'
            self.HELP_MOVE = 'Moves a song from position pos1 to pos2 in queue.'
            self.HELP_MOVE_LONG = 'Moves a song from position pos1 to pos2 in queue.'
            self.HELP_REMOVE = 'Remove a song at position x.'
            self.HELP_REMOVE_LONG = 'Remove a song at position x.'
            self.HELP_RESET = 'Reset the Player of the server.'
            self.HELP_RESET_LONG = 'Reset the Player of the server. Useful for debugging'
            self.HELP_HELP = f'Use {config.BOT_PREFIX}help <command> for more info.'
            self.HELP_HELP_LONG = f'Nice recursion bro'
            self.HELP_INVITE = 'Send invite URL'
            self.HELP_INVITE_LONG = 'Sends bot invite link'
            self.HELP_WAHL = 'Ask the "Heilige Wahlkommission" a question'
            self.HELP_WAHL_LONG = 'Asks the "Heilige Wahlkommission" for salvation and enlightenment.'
            self.HELP_ALERT = 'Pings you after some time.'
            self.HELP_ALERT_LONG = 'Pings you after some time. Syntax: [1-60][s,m,h,d] (ID/Message) (Message).'
            self.HELP_CLEAN = 'Cleans messages sent by bot and bot commands'
            self.HELP_CLEAN_LONG = (f'Cleans messages sent by bot and bot commands.\nSyntax: {config.BOT_PREFIX}clean [(user,bot,all,any,saul) (n)]'
                                    f', defaults are all, 20.\nArgument order doesn\'t matter.\nQueries the last {config.CLEAN_AMOUNT} messages.\n\n'
                                    f'user = messages that start with "{config.BOT_PREFIX}"\nbot = messages by bot\nall = both\n'
                                    f'any = any message (effectively a purge command)\nsaul = messages from saul goodman as he likes to spam')
            self.HELP_RESTART = 'Restart the bot.'
            self.HELP_RESTART_LONG = 'Restarts the bot. Can only be used by bot admins.'
            self.HELP_BAN = 'Bans a user from using Blueshellbot.'
            self.HELP_BAN_LONG = ('Bans a user from using the bot. Any command they run will not work and will not be executed.\n'
                                  'If the command is used again, the user will be unbanned.\n'
                                  'Syntax: `b.ban <user_id>`'
                                  'This command is admin only')
            self.HELP_FORCE_EMBED = 'Forces any embed for testing purposes.'
            self.HELP_FORCE_EMBED_LONG = (f'Run `{config.BOT_PREFIX}force_embed list` to display all available embeds.'
                                          f'Run `{config.BOT_PREFIX}force_embed <embed>` to show any embed. This command is admin only.')
            self.HELP_FEET = 'laal.'
            self.HELP_FEET_LONG = 'Maggda loves feets and loves briar imagine he had brier feets aka YOU CANT PLURALS YOU CAKE SNAKE SKIBIDI SEVERUS SNAPE'
            self.HELP_CONVKANA = 'Converts kana into romaji or the other way around.'
            self.HELP_CONVKANA_LONG = (f'Converts between hiragana/katakana and romaji.\n'
                                       f'Syntax: `{config.BOT_PREFIX}convkana [h/k] <kana/romaji>`\n'
                                       f'Example: `{config.BOT_PREFIX}convkana h りょ` returns "ryo"\n'
                                       f'Works with multiple kana.')
            self.HELP_KANA_GAME = 'Starts the kana game.'
            self.HELP_KANA_GAME_LONG = (f'Starts an interactive game for guessing kana.\n'
                                        f'Syntax: `{config.BOT_PREFIX}kanagame [h/k/b] [t/f/b]`\n'
                                        f'Letter meanings: hiragana, katakana, both | to, from, both')

            self.HELP_PINSERT = 'Inserts a new command into pizza romani.'
            self.HELP_PINSERT_LONG = (f'Adds a new command into pizza romani.\n'
                                      f'Syntax: `{config.BOT_PREFIX}pinsert "to_match" "response"`\n'
                                      f'Example: `{config.BOT_PREFIX}pinsert "in test | is bomboclaat" "test icles"`\n'
                                      f'If message and/or response have spaces in it, use quotation marks.')

            self.HELP_PLIST = 'Lists pizza romani matches, with further options.'
            self.HELP_PLIST_LONG = (f'Lists all pizza romani matches. You can provide arguments to search further.\n\n'
                                    f'Syntax: `{config.BOT_PREFIX}plist (filter keyword)`\n'
                                    f'Example: `{config.BOT_PREFIX}plist write "test icles"`\n\n'
                                    f'Possible search filters are:\n'
                                    f'author (id/ping)\n'
                                    f'read (what it matches)\n'
                                    f'write (what it replies with)\n'
                                    f'type (which match type)\n')

            self.HELP_PINFO = 'Gets info about one pizza command.'
            self.HELP_PINFO_LONG = (f'Retrieves information about one pizza romani command.\n'
                                    f'You can find this command by searching for its write value.\n\n'
                                    f'Syntax: `{config.BOT_PREFIX}pinfo write_value (number)`\n'
                                    f'Example: `{config.BOT_PREFIX}pinfo "test icles" 2\n\n'
                                    f'If there are 2 or more commands with the same write value '
                                    f'(you can find them by running and filtering `{config.BOT_PREFIX}plist`), '
                                    f'enter a number after the first argument to select different ones.')

            self.HELP_PREMOVE = 'Removes a command from pizza romani.'
            self.HELP_PREMOVE_LONG = ('Remove a command.\n\n'
                                      f'Syntax: `{config.BOT_PREFIX}premove write_value (number)`'
                                      f'Example: `{config.BOT_PREFIX}premove "test icles" 2`\n\n'
                                      f'If there are 2 or more commands with the same write value '
                                      f'(you can find them by running and filtering `{config.BOT_PREFIX}plist`), '
                                      f'enter a number after the first argument to select different ones.')

            self.HELP_COMPILER = 'Tests the pizza romani compiler.'
            self.HELP_COMPILER_LONG = ('Allows direct interaction with the pizza romani compiler.\n\n'
                                       f'Syntax: `{config.BOT_PREFIX}ptestcompiler condition message`\n'
                                       f'Example: `{config.BOT_PREFIX}ptestcompiler "in a & (in b | end c)" "ac"`\n\n'
                                       f'Automatically uses complex type. Have fun maggda')

            self.SLASH_QUEUE_DESCRIPTION = f'Number of queue page, there are only {config.MAX_SONGS_IN_PAGE} songs by page'
            self.SLASH_MOVE_HELP = 'Moves a song from position pos1 to pos2 in queue.'
