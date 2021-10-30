from .square import Square, SquareType, Room, Animal, RoomType
from typing import List
import random


class Board:

    TOTAL_SQUARES = 76

    TRAPS = [7, 14, 27, 34]
    STARTING_SQUARES = [1, 21, 41, 59, 20, 40, 77]

    ROOM_LIVING = [63, 44, 10]
    ROOM_CELLAR = [5]
    ROOM_LABORATORY = [24]
    ROOM_PANTHEON = [30, 55, 73]
    ROOM_LIBRARY = [36]
    ROOM_GARAGE = [18]
    ROOM_BEDROOM = [68]

    # players is a list
    def __init__(self, players: List[str]):
        self.squares = []
        self.players = {}

        # Assign random starting squares to players
        for p in players:
            i = random.randrange(0, len(self.STARTING_SQUARES))
            self.players[p] = self.STARTING_SQUARES[i]
            self.STARTING_SQUARES.pop(i)

        # Init board squares
        for i in range(self.TOTAL_SQUARES):
            if i in self.ROOM_LIVING:
                self.squares[i] = Room(i, RoomType.LIVING)
            elif i in self.ROOM_BEDROOM:
                self.squares[i] = Room(i, RoomType.BEDROOM)
            elif i in self.ROOM_CELLAR:
                self.squares[i] = Room(i, RoomType.CELLAR)
            elif i in self.ROOM_LABORATORY:
                self.squares[i] = Room(i, RoomType.LABORATORY)
            elif i in self.ROOM_PANTHEON:
                self.squares[i] = Room(i, RoomType.PANTHEON)
            elif i in self.ROOM_LIBRARY:
                self.squares[i] = Room(i, RoomType.LIBRARY)
            elif i in self.ROOM_GARAGE:
                self.squares[i] = Room(i, RoomType.GARAGE)
            elif i in self.TRAPS:
                self.squares[i] = Square(i, SquareType.TRAP)
            else:
                self.squares[i] = Square(i, SquareType.REGULAR)

    def move_player(self, position, player_name) -> Square:
        self.players[player_name] = position
        return self.squares[self.players[player_name]]

    def get_player_position(self, player_name) -> Square:
        return self.squares[self.players[player_name]]
