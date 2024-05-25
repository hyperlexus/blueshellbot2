from enum import Enum
from typing import Tuple


class BCommandsType(Enum):
    PREV = 'Prev'
    SKIP = 'Skip'
    PAUSE = 'Pause'
    RESUME = 'Resume'
    CONTEXT = 'Context'
    PLAY = 'Play'
    STOP = 'Stop'
    RESET = 'Reset'
    NOW_PLAYING = 'Now Playing'
    TERMINATE = 'Terminate'
    VOLUME = 'Volume'
    SLEEPING = 'Sleeping'


class BCommands:
    def __init__(self, type: BCommandsType, args=None) -> None:
        self.__type = type
        self.__args = args

    def getType(self) -> BCommandsType:
        return self.__type

    def getArgs(self) -> Tuple:
        return self.__args
