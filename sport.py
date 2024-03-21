from enum import Enum

class Sport:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation


class SportEnum(Enum):
    BASEBALL = 1
    MCROSSCOUNTRY = 2
    FENCING = 3
    FIELDHOCKEY = 4
    FOOTBALL = 5
    GYMNASTICS = 6
    MBASKETBALL = 7
    MGOLF = 8
    MLACROSSE = 9
    MSOCCER = 10
    MTENNIS = 11
    MOUTDOORTF = 12
    WOUTDOORTF = 13
    SOFTBALL = 14
    MSWIMDIVE = 15
    WSWIMDIVE = 16
    WBASKETBALL = 17
    WGOLF = 18
    WLAX = 19
    WROWING = 20
    WSOCCER = 21
    WTENNIS = 22
    WVOLLEYBALL = 23
    WRESTLING = 24