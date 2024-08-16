from Config.Singleton import Singleton


class BColors(Singleton):
    def __init__(self) -> None:
        self.__purple = 0x8848FF
        self.__red = 0xDC143C
        self.__green = 0x1F8B4C
        self.__grey = 0x708090
        self.__blue = 0x206694
        self.__black = 0x23272A

    @property
    def GREEN(self) -> str:
        return self.__green

    @property
    def GREY(self) -> str:
        return self.__grey

    @property
    def BLUE(self) -> str:
        return self.__blue

    @property
    def BLACK(self) -> str:
        return self.__black

    def PURPLE(self) -> str:
        return self.__purple

    @property
    def RED(self) -> str:
        return self.__red
