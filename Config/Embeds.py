from random import random
from datetime import timedelta
from discord import Embed

from Config.Messages import Messages
from Config.Exceptions import BlueshellError
from Config.Configs import BConfigs
from Config.Colors import BColors
from Utils.PizzaEval.PizzaEvalUtils import identify_error
from Utils.PizzaEval.PizzaEvalErrorDict import error_dict


class BEmbeds:
    def __init__(self) -> None:
        self.__config = BConfigs()
        self.__messages = Messages()
        self.__colors = BColors()

    def BAD_COMMAND_USAGE(self, command_name: str):
        embed = Embed(
            title="Incorrect command usage",
            description=f"You cannot use this command like that.\n"
                        f"Check `{self.__config.BOT_PREFIX}help {command_name}` for more information.",
            color=self.__colors.RED
        )
        return embed

    def __willShowProject(self) -> bool:
        return random() * 100 < self.__config.CHANCE_SHOW_TEXT

    def __addFooterContent(self, embed: Embed) -> Embed:
        footerText = f'\u200b Fun fact: this text has a 1/100 chance of appearing'
        return embed.set_footer(text=footerText, icon_url=self.__config.SUPPORTING_ICON)

    def ONE_SONG_LOOPING(self, info: dict) -> Embed:
        title = self.__messages.ONE_SONG_LOOPING
        return self.SONG_INFO(info, title)

    def EMPTY_QUEUE(self) -> Embed:
        title = self.__messages.SONG_PLAYER
        text = self.__messages.EMPTY_QUEUE
        embed = Embed(
            title=title,
            description=text,
            colour=self.__colors.BLUE
        )
        return embed

    def MISSING_ARGUMENTS(self) -> Embed:
        embed = Embed(
            title="Missing some arguments",
            description="🥶 This command did not receive the correct amount of arguments. Please try again.",
            colour=self.__colors.RED
        )
        return embed

    def INVALID_INDEX(self) -> Embed:
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.INVALID_INDEX,
            colour=self.__colors.BLACK
        )
        return embed

    def SONG_ADDED_TWO(self, info: dict, pos: int) -> Embed:
        embed = self.SONG_INFO(info, self.__messages.SONG_ADDED_TWO, pos)
        return embed

    def INVALID_INPUT(self) -> Embed:
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.INVALID_INPUT,
            colour=self.__colors.BLACK)
        return embed

    def UNAVAILABLE_VIDEO(self) -> Embed:
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.VIDEO_UNAVAILABLE,
            colour=self.__colors.BLACK)
        return embed

    def DOWNLOADING_ERROR(self) -> Embed:
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.DOWNLOADING_ERROR,
            colour=self.__colors.BLACK)
        return embed

    def SONG_ADDED(self, title: str) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.SONG_ADDED.format(title),
            colour=self.__colors.BLUE)
        return embed

    def SONGS_ADDED(self, quant: int) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.SONGS_ADDED.format(quant),
            colour=self.__colors.BLUE)
        return embed

    def SONG_INFO(self, info: dict, title: str, position='0') -> Embed:
        embedvc = Embed(
            title=title,
            description=f"[{info['title']}]({info['original_url']})",
            colour=self.__colors.BLUE
        )

        embedvc.add_field(name=self.__messages.SONGINFO_UPLOADER,
                          value=info['uploader'],
                          inline=False)

        embedvc.add_field(name=self.__messages.SONGINFO_REQUESTER,
                          value=info['requester'],
                          inline=True)

        if 'thumbnail' in info.keys():
            embedvc.set_thumbnail(url=info['thumbnail'])

        if 'duration' in info.keys():
            duration = str(timedelta(seconds=info['duration']))
            embedvc.add_field(name=self.__messages.SONGINFO_DURATION,
                              value=f"{duration}",
                              inline=True)
        else:
            embedvc.add_field(name=self.__messages.SONGINFO_DURATION,
                              value=self.__messages.SONGINFO_UNKNOWN_DURATION,
                              inline=True)

        embedvc.add_field(name=self.__messages.SONGINFO_POSITION,
                          value=position,
                          inline=True)

        if self.__willShowProject():
            embedvc = self.__addFooterContent(embedvc)
        return embedvc

    def SONG_MOVED(self, song_name: str, pos1: int, pos2: int) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.SONG_MOVED_SUCCESSFULLY.format(song_name, pos1, pos2),
            colour=self.__colors.BLUE
        )
        return embed

    def ERROR_MOVING(self) -> Embed:
        embed = Embed(
            title=self.__messages.UNKNOWN_ERROR,
            description=self.__messages.ERROR_MOVING,
            colour=self.__colors.BLACK
        )
        return embed

    def ERROR_EMBED(self, description: str) -> Embed:
        embed = Embed(
            description=description,
            colour=self.__colors.BLACK
        )
        return embed

    def CUSTOM_ERROR(self, error: BlueshellError) -> Embed:
        embed = Embed(
            title=error.title,
            description=error.message,
            colour=self.__colors.BLACK
        )
        return embed

    def WRONG_LENGTH_INPUT(self) -> Embed:
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.LENGTH_ERROR,
            colour=self.__colors.BLACK
        )
        return embed

    def BAD_LOOP_USE(self) -> Embed:
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.BAD_USE_OF_LOOP,
            colour=self.__colors.BLACK
        )
        return embed

    def COMMAND_ERROR(self):
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.ERROR_MISSING_ARGUMENTS,
            colour=self.__colors.BLACK
        )
        return embed

    def INVALID_ARGUMENTS(self):
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.INVALID_ARGUMENTS,
            colour=self.__colors.BLACK
        )
        return embed

    def COMMAND_NOT_FOUND(self) -> Embed:
        embed = Embed(
            title=self.__messages.COMMAND_NOT_FOUND_TITLE,
            description=self.__messages.COMMAND_NOT_FOUND,
            colour=self.__colors.BLACK
        )
        return embed

    def MY_ERROR_BAD_COMMAND(self) -> Embed:
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.BAD_COMMAND,
            colour=self.__colors.BLACK
        )
        return embed

    def UNKNOWN_ERROR(self, error_type=None) -> Embed:
        desc_addon = f"\n\nerror type: {error_type}" if error_type else ""
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.UNKNOWN_ERROR + desc_addon,
            colour=self.__colors.RED
        )
        return embed

    def FAIL_DUE_TO_LOOP_ON(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.LOOP_ON,
            colour=self.__colors.BLACK
        )
        return embed

    def ERROR_SHUFFLING(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.ERROR_SHUFFLING,
            colour=self.__colors.BLACK
        )
        return embed

    def SONGS_SHUFFLED(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.SONGS_SHUFFLED,
            colour=self.__colors.BLUE
        )
        return embed

    def LOOP_ONE_ACTIVATED(self) -> Embed:
        embed = Embed(
            title=self.__messages.LOOP_ONE_ACTIVATE,
            colour=self.__colors.BLUE
        )
        return embed

    def LOOP_ALL_ACTIVATED(self) -> Embed:
        embed = Embed(
            title=self.__messages.LOOP_ALL_ACTIVATE,
            colour=self.__colors.BLUE
        )
        return embed

    def SONG_PROBLEMATIC(self) -> Embed:
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.DOWNLOADING_ERROR,
            colour=self.__colors.BLACK)
        return embed

    def PLAYER_RESTARTED(self) -> Embed:
        embed = Embed(
            title=self.__messages.ERROR_TITLE,
            description=self.__messages.ERROR_IN_PROCESS,
            colour=self.__colors.BLACK)
        return embed

    def NO_CHANNEL(self) -> Embed:
        embed = Embed(
            title=self.__messages.IMPOSSIBLE_MOVE,
            description=self.__messages.NO_CHANNEL,
            colour=self.__colors.BLACK
        )
        return embed

    def ERROR_DUE_LOOP_ONE_ON(self) -> Embed:
        embed = Embed(
            title=self.__messages.BAD_COMMAND_TITLE,
            description=self.__messages.ERROR_DUE_LOOP_ONE_ON,
            colour=self.__colors.BLACK
        )
        return embed

    def LOOP_DISABLE(self) -> Embed:
        embed = Embed(
            title=self.__messages.LOOP_DISABLE,
            colour=self.__colors.BLUE
        )
        return embed

    def PLAYER_RESUMED(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_RESUMED,
            colour=self.__colors.BLUE
        )
        return embed

    def SKIPPING_SONG(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_SKIPPED,
            colour=self.__colors.BLUE
        )
        return embed

    def STOPPING_PLAYER(self) -> Embed:
        embed = Embed(
            title=self.__messages.STOPPING,
            colour=self.__colors.BLUE
        )
        return embed

    def RETURNING_SONG(self) -> Embed:
        embed = Embed(
            title=self.__messages.RETURNING_SONG,
            colour=self.__colors.BLUE
        )
        return embed

    def PLAYER_PAUSED(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PAUSED,
            colour=self.__colors.BLUE
        )
        return embed

    def NOT_PREVIOUS_SONG(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.NOT_PREVIOUS,
            colour=self.__colors.BLUE
        )
        return embed

    def HISTORY(self, description: str) -> Embed:
        embed = Embed(
            title=self.__messages.HISTORY_TITLE,
            description=description,
            colour=self.__colors.BLUE)
        return embed

    def NOT_PLAYING(self) -> Embed:
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.PLAYER_NOT_PLAYING,
            colour=self.__colors.BLUE)
        return embed
    
    def VOLUME_CHANGED(self, volume: float) -> Embed:
        if isinstance(volume, float) and volume == int(volume):
            volume = int(volume)
        embed = Embed(
            title=self.__messages.SONG_PLAYER,
            description=self.__messages.VOLUME_CHANGED.format(volume),
            colour=self.__colors.BLUE)
        return embed

    def QUEUE(self, title: str, description: str) -> Embed:
        embed = Embed(
            title=title,
            description=description,
            colour=self.__colors.BLUE
        )

        if self.__willShowProject():
            embed = self.__addFooterContent(embed)
        return embed

    def INVITE(self, bot_id: str) -> Embed:
        link = self.__messages.INVITE_URL
        link.format(bot_id)
        text = self.__messages.INVITE_MESSAGE.format(link, link)

        embed = Embed(
            title="Invite Blueshell",
            description=text,
            colour=self.__colors.BLUE
        )
        return embed

    def ERROR_NUMBER(self) -> Embed:
        embed = Embed(
            description=self.__messages.ERROR_NUMBER,
            colour=self.__colors.BLACK
        )
        return embed

    def RANDOM_NUMBER(self, a: int, b: int, x: int) -> Embed:
        embed = Embed(
            title=f'Random number between [{a}, {b}]',
            description=x,
            colour=self.__colors.GREEN
        )
        return embed

    def SONG_REMOVED(self, song_name: str) -> Embed:
        embed = Embed(
            description=self.__messages.SONG_REMOVED_SUCCESSFULLY.format(song_name),
            colour=self.__colors.BLUE
        )
        return embed

    def PLAYLIST_RANGE_ERROR(self) -> Embed:
        embed = Embed(
            description=self.__messages.LENGTH_ERROR,
            colour=self.__colors.BLACK
        )
        return embed

    def PLAYLIST_CLEAR(self) -> Embed:
        return Embed(
            description=self.__messages.PLAYLIST_CLEAR
        )

    def WAHLKOMMISSION(self, result: str) -> Embed:
        embed = Embed(
            title='Die heilige Wahlkommission hat entschieden!',
            description=f'Zahl: {result}',
            colour=self.__colors.GREEN
        )
        embed.set_footer(text='Pizza Romani reference.')
        return embed

    def ALERT_SET(self, time_str: str) -> Embed:
        embed = Embed(
            title='Alert',
            description=f"✅ Timer set for in {time_str}",
            colour=self.__colors.GREEN
        )
        return embed

    def ALERT_DONE(self, *args: tuple) -> Embed:
        time_str = args[0]
        message = args[1] if len(args) > 1 and args[1] else None

        description = f"⏰ Alert of {time_str} done"
        description += f", message is: {message}." if message else "."

        embed = Embed(
            title="Alert",
            description=description,
            colour=self.__colors.GREEN
        )
        return embed

    def BAD_ALERT(self, time_str: str) -> Embed:
        embed = Embed(
            title='Bad alert usage',
            description=f'You cannot use {time_str} as an alert input. Use {self.__config.BOT_PREFIX}help alert.',
            colour=self.__colors.RED
        )
        return embed

    def SESSION_CLOSED(self) -> Embed:
        embed = Embed(
            title='Session closed',
            description='A command or ongoing function was disabled because the session closed.',
            colour=self.__colors.RED
        )
        return embed

    def BAD_ABSOLUTE_ALERT(self) -> Embed:
        embed = Embed(
            title='Bad alert usage',
            description=self.__messages.BAD_ABSOLUTE_ALERT,
            colour=self.__colors.RED
        )
        return embed

    def BAD_USER_ID(self, user_id: str) -> Embed:
        embed = Embed(
            title='Bad User ID',
            description=f'User ID "{user_id}" didn\'t work. Right click someone to copy their ID, or ping them.',
            colour=self.__colors.RED
        )
        return embed

    def CLEANED(self, num: int, count: int, sender: str, inspected: int) -> Embed:
        embed = Embed(
            title='🪥 Cleaned',
            description=f'Queried {num} message{" " if num == 1 else "s "} with the "{sender}" flag, cleaned {count}. Inspected {inspected} message{" " if inspected == 1 else "s "}',
            colour=self.__colors.GREEN
        )
        return embed

    def BAD_CLEAN_INPUT(self, *args: tuple):
        arg_str = ''
        if len(args) > 0:
            for i in args:
                arg_str += f", {i}"
        else:
            arg_str = 'None'
        embed = Embed(
            title='Bad clean command input',
            description=f'This input doesn\'t work. Args passed: {arg_str}',
            colour=self.__colors.RED
        )
        embed.set_footer(text="How did you even get here. That command literally shouldn't fail")
        return embed

    def TOO_MANY_CLEAN_QUERIES(self, limit: int):
        embed = Embed(
            title='Bad clean command input',
            description=f'Number to clean ({limit}) exceeds messages inspected ({self.__config.CLEAN_AMOUNT}). Operation not performed.',
            colour=self.__colors.RED
        )
        return embed

    def MISSING_PERMISSIONS(self, command_name):
        embed = Embed(
            title=f'Error: Use of {self.__config.BOT_PREFIX}{command_name} is forbidden for this user',
            description='You do not have the necessary permission to run this command.',
            color=self.__colors.RED
        )
        return embed

    def SUCCESSFUL_BAN(self, username):
        embed = Embed(
            title=f'Successfully banned user {username}.',
            description='This user will now be unable to access blueshellbot.',
            color=self.__colors.BLUE
        )
        return embed

    def SUCCESSFUL_UNBAN(self, username):
        embed = Embed(
            title=f'Successfully unbanned user {username}.',
            description='This user will now be able to access blueshellbot again.',
            color=self.__colors.BLUE
        )
        return embed

    def INVALID_BAN_COMMAND(self):
        embed = Embed(
            title=f'Error: You cannot ban yourself or other bot admins.',
            color=self.__colors.RED
        )
        return embed

    def BANNED(self):
        embed = Embed(
            title=f'Error: You are banned',
            description=f'You are banned from blueshellbot and cannot run this command.',
            color=self.__colors.RED
        )
        return embed

    def KANA_CONVERTED_EMBED(self, conv_from, conv_to, kana_type, success_code):
        if success_code == 0:
            description_text = f'{conv_from} -> {conv_to} ({"hiragana" if kana_type == "h" else "katakana"})'
            color_to_set = self.__colors.GREEN
        else:
            description_text = (f'Could not or only partially convert input "{conv_from}".\n'
                                f'{conv_to} ({"hiragana" if kana_type == "h" else "katakana"})')
            color_to_set = self.__colors.RED
        embed = Embed(
            title=f'Kana conversion',
            description=description_text,
            color=color_to_set
        )
        return embed

    def PIZZA_INSERTED(self, read, write, replace):
        embed = Embed(
            title="Successfully inserted a new command into pizza romani!",
            description=f"{read} -> {write}{' (replace mode on)' if replace else ''}",
            color=self.__colors.BLUE
        )
        return embed

    def PIZZA_LIST_TOO_LONG(self):
        embed = Embed(
            title="Error: list too long",
            description="The list of commands is too long. Try narrowing down your search results!",
            color=self.__colors.RED
        )
        return embed

    def PIZZA_LIST(self, text):
        embed = Embed(
            title="List of pizza commands",
            description=text,
            color=self.__colors.BLUE
        )
        return embed

    def PIZZA_LIST_FILTERED(self, text, filter_type, filter_keyword):
        embed = Embed(
            title="List of pizza commands",
            description=f"Filtered by {filter_type}, matching {filter_keyword}\n\n{text}",
            color=self.__colors.BLUE
        )
        return embed

    def PIZZA_INFO(self, text):
        embed = Embed(
            title="Information on a pizza command",
            description=text,
            color=self.__colors.BLUE
        )
        return embed

    def INTEGER_ONLY_HERE(self, not_an_int):
        embed = Embed(
            title="Error: an integer is required here.",
            description=f"The input {not_an_int} is not an integer. Please only input integers here.",
            color=self.__colors.RED
        )
        return embed

    def PREMOVE_NOT_SPECIFIED(self):
        embed = Embed(
            title="Error: more than 1 option",
            description="The command you are trying to remove has more than 1 match. Please specify a number as second argument.",
            color=self.__colors.RED
        )
        return embed

    def PIZZA_INVALID_INPUT(self, error_code, expression):
        embed = Embed(
            title="Error: Pizza Romani input not valid.",
            description="The input did not satisfy all requirements. Problem: \n\n" + identify_error(error_code, expression),
            color=self.__colors.RED
        )
        embed.set_footer(text="Check if you made a typo or are maybe missing a space.",
                         icon_url="https://static-00.iconduck.com/assets.00/cold-face-emoji-512x512-k8er8wn9.png")
        return embed

    def PIZZA_MOD_LIST_ERROR_DICT(self):
        embed = Embed(
            title='Forced embed: Error dict for complex evaluator',
            description="\n".join(f"{code}: {message}" for code, message in error_dict.items()),
            color=self.__colors.BLUE
        )
        return embed

    def TURNED_REPLACE_OFF(self):
        embed = Embed(
            title='Information: replace mode turned off',
            description="'complex' mode does not support replace mode, therefore it has been turned off.'",
            color=self.__colors.GREY
        )
        return embed

    def NO_CLOSING_QUOTE(self):
        embed = Embed(
            title="Error: no closing quote provided",
            description="One of your arguments does not have a closing quote. Close all opened quotes, and try again.",
            color=self.__colors.RED
        )
        embed.set_footer(text="If that was on purpose, please do not purpose", icon_url="https://cdn.discordapp.com/emojis/1126999492131029033.webp?size=96")
        return embed

    def PREMOVE_NO_COMMAND_FOUND(self, remove_str: str):
        embed = Embed(
            title="Nothing found when trying to remove a command",
            description=f"Query {remove_str} matched no commands",
            color=self.__colors.BLUE
        )
        return embed

    def PREMOVE_REMOVED(self, command_str: str, number=None):
        desc_addon = f", number {number}" if number else ""
        embed = Embed(
            title="Removed a command from Pizza Romani",
            description=f"Removed command `{command_str}`" + desc_addon,
            color=self.__colors.GREEN
        )
        return embed

    def PREMOVE_NUMBER_LARGER_THAN_AMOUNT_COMMANDS(self, number: int, command_amount: int):
        embed = Embed(
            title="Error: Number specified was larger than the amount of matching commands",
            description=f"Yea the title kinda says it all, you gave {number} but there are {command_amount} commands.",
            color=self.__colors.RED
        )
        return embed
