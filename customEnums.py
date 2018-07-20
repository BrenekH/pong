from enum import Enum

class GameModes(Enum):
    twoPlayers = 0
    onePlayer = 1
    zeroPlayers = 2

class BotDiffs(Enum):
    easy = 0
    medium = 1
    hard = 2
    impossible = 3