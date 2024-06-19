from enum import Enum


class ConsoleColor(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    Bright_Black = 90
    Bright_Red = 91
    Bright_Green = 92
    Bright_Yellow = 93
    Bright_Blue = 94
    Bright_Magenta = 95
    Bright_Cyan = 96
    Bright_White = 97
    Default = 39


class TextMode(Enum):
    Default = 0
    Bold = 1
    dim = 2
    Italic = 3
    Underline = 4
    Blinking = 5
    Reverse = 7
    Hidden = 8
    StrikeThrough = 9


class ResetMode(Enum):
    ResetAll = 0
    NoReset = -1
    Bold = 21
    Dim = 22
    Italic = 23
    Underline = 24
    Blinking = 25
    Reverse = 27
    Hidden = 28
    StrikeThrough = 29