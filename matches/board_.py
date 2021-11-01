from .square import Square, SquareType
from typing import List
from util.vector import Vector2d
import random


class Board:

    WIDTH = 20
    HEIGHT = 20

    TRAPS = [(6, 6), (13, 6), (6, 13), (13, 13)]
    STARTING_SQUARES = [(0, 6), (6, 0), (13, 0), (0, 13), (19, 6), (6, 19), (19, 13), (13, 19)]

    ROOM_LIVING = [(3, 6), (6, 9), (4, 13)]
    ROOM_CELLAR = [(6, 4)]
    ROOM_LABORATORY = [(13, 3)]
    ROOM_PANTHEON = [(16, 6), (13, 9), (15, 13)]
    ROOM_LIBRARY = [(13, 15)]
    ROOM_GARAGE = [(6, 17)]
    ROOM_BEDROOM = [(10, 13)]
    ROOM_DINING = [(10, 6)]

    def __init__(self, players: List[str]):
        self.squares = []
        # {'player_name': Vector2d(x, y), ... }
        self.players = {}

        # Assign random starting squares to players
        for p in players:
            i = random.randrange(0, len(self.STARTING_SQUARES))
            self.players[p] = Vector2d(self.STARTING_SQUARES[i][0], self.STARTING_SQUARES[i][1])
            self.STARTING_SQUARES.pop(i)

        # Init board squares
        for i in range(0, self.WIDTH):
            sublist = []
            for j in range(0, self.HEIGHT):
                # Some coordinates aren't supposed to have squares in them, so we fill with None
                if (i < 6 or 6 < i < 13 or i > 13) and (j < 6 or 13 > j > 6 or j > 13):
                    sublist.append(None)
                else:
                    sublist.append(self.__get_room(i, j))
            self.squares.append(sublist)

    def __get_room(self, i, j):
        if (i, j) in self.ROOM_LIVING:
            room = Square(SquareType.LIVING)
        elif (i, j) in self.ROOM_BEDROOM:
            room = Square(SquareType.BEDROOM)
        elif (i, j) in self.ROOM_CELLAR:
            room = Square(SquareType.CELLAR)
        elif (i, j) in self.ROOM_LABORATORY:
            room = Square(SquareType.LABORATORY)
        elif (i, j) in self.ROOM_PANTHEON:
            room = Square(SquareType.PANTHEON)
        elif (i, j) in self.ROOM_LIBRARY:
            room = Square(SquareType.LIBRARY)
        elif (i, j) in self.ROOM_GARAGE:
            room = Square(SquareType.GARAGE)
        elif (i, j) in self.ROOM_DINING:
            room = Square(SquareType.DINING)
        elif (i, j) in self.TRAPS:
            room = Square(SquareType.TRAP)
        else:
            room = Square(SquareType.REGULAR)

        return room

    def move_player(self, position: Vector2d, player_name) -> Square:
        self.players[player_name] = position

        return self.squares[position.x][position.y]

    def get_player_position(self, player_name) -> Vector2d:
        return self.players[player_name]

    def get_player_square(self, player_name) -> Square:
        p = self.players[player_name]
        return self.squares[p.x][p.y]
