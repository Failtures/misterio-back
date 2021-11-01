from enum import Enum


class SquareType(Enum):
    NONE = 0
    REGULAR = 1
    TRAP = 2
    ANIMAL = 3
    LIVING = 4
    CELLAR = 5
    LABORATORY = 6
    PANTHEON = 7
    LIBRARY = 8
    GARAGE = 9
    BEDROOM = 10
    DINING = 11


class Square:

    def __init__(self, squaretype: SquareType):
        self.squaretype = squaretype

    def __str__(self):
        return (str(self.squaretype.name)).lower().title()
