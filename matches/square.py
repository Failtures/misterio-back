from enum import Enum


class SquareType(Enum):
    REGULAR = 1
    ROOM = 2
    TRAP = 3
    ANIMAL = 4


class RoomType(Enum):
    LIVING = 1
    CELLAR = 2
    LABORATORY = 3
    PANTHEON = 4
    LIBRARY = 5
    GARAGE = 6
    BEDROOM = 7


class Square:

    def __init__(self, position, squaretype: SquareType):
        self.position = position
        self.squareType = squaretype


class Room(Square):

    def __init__(self, position: int, roomtype: RoomType):
        super().__init__(position, SquareType.ROOM)
        self.roomtype = roomtype


class Animal(Square):

    def __init__(self, position: int, name: str):
        super().__init__(position, SquareType.ANIMAL)
