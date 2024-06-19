import sys
from .utils_enum import *


class Console:
    def __new__(cls):
        raise TypeError("Console Class cannot be instantiated directly")

    @staticmethod
    def Print16C(content: object, textcolor=ConsoleColor.Default,
                 background=ConsoleColor.Default, textmode=TextMode.Default, resetmode=ResetMode.NoReset,
                 end="\n") -> None:
        """
        Print the contents on the console/terminal in ANSI 16 color format.
        :param content: Python Printable object(str, int, list or tuple, etc)
        :param textcolor: Any ConsoleColor Enum
        :param background: Any ConsoleColor Enum
        :param textmode: Any TextMode  Enum
        :param resetmode: Any ResetMode  Enum
        :param end:

        :return: None
        """
        endcode = f"\033[{resetmode.value}m{end}"
        if resetmode == ResetMode.NoReset:
            endcode = f"{end}"

        colorcode = f"\033[{textmode.value};" + str(textcolor.value) + ";" + str(background.value + 10) + "m"
        if textcolor == ConsoleColor.Default and background == ConsoleColor.Default:
            colorcode = ""

        sys.stdout.write(colorcode + str(content) + endcode)

    @staticmethod
    def Print256C(content: object, textcolor: int = None, background: int = None, textmode=TextMode.Default,
                  resetmode=ResetMode.NoReset, end="\n") -> None:
        """
        Print the contents on the console/terminal in ANSI 256 color format.

        :param content: Python Printable object(str, int, list or tuple, etc)
        :param textcolor: 0 - 255 int
        :param background: 0 - 255 int
        :param textmode: Any TextMode  Enum
        :param resetmode: Any ResetMode  Enum
        :param end:

        :return: None
        """
        endcode = f"\033[{resetmode.value}m{end}"
        if resetmode == ResetMode.NoReset:
            endcode = f"{end}"

        code = ""
        if (textcolor is not None) and (background is not None):
            code = f"\033[{textmode.value};38;5;{textcolor};48;5;{background}m"
        elif textcolor is not None:
            code = f"\033[{textmode.value};38;5;{textcolor}m"
        elif background is not None:
            code = f"\033[{textmode.value};48;5;{background}m"

        sys.stdout.write(code + str(content) + endcode)

    @staticmethod
    def Printrgb(content: object, textcolor: tuple = None, background: tuple = None, textmode=TextMode.Default,
                 resetmode=ResetMode.NoReset, end="\n") -> None:
        """
        Print the contents on the console/terminal in ANSI RGb color format.
        :param content:
        :param textcolor:
        :param background:
        :param textmode:
        :param resetmode:
        :param end:

        :return: None
        """

        endcode = f"\033[{resetmode.value}m{end}"
        if resetmode == ResetMode.NoReset:
            endcode = f"{end}"

        colorcode = ""
        if (textcolor is not None) and (background is not None):
            colorcode = f"\033[{textmode.value};38;2;{textcolor[0]};{textcolor[1]};{textcolor[2]};48;2;{background[0]};{background[1]};{background[2]}m"
        elif textcolor is not None:
            colorcode = f"\033[{textmode.value};38;2;{textcolor[0]};{textcolor[1]};{textcolor[2]}m"
        elif background is not None:
            colorcode = f"\033[{textmode.value};48;2;{background[0]};{background[1]};{background[2]}m"

        sys.stdout.write(colorcode + str(content) + endcode)

