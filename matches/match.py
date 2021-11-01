import random
from typing import List
from users.user import User
from .board_ import Board
from util.vector import Vector2d


class Match:

    def __init__(self, name: str, players: List[User]):
        self._current_turn = 0
        self._rolled_dice = False
        self._moved = False
        self._current_roll = 0

        self.name = name
        self.players = players
        self.board = Board([p.nickname for p in players])

        # Shuffle turn order
        random.shuffle(self.players)

    def __eq__ (self, other):
        return self.name == other.name

    def next_turn(self) -> User:
        self._current_turn += 1
        self._current_turn %= len(self.players)
        # Reset flags
        self._rolled_dice = False
        self._moved = False

        return self.current_turn()

    def roll_dice(self) -> int:
        if self._rolled_dice:
            raise Exception('Already rolled dice this turn')
        self._rolled_dice = True
        self._current_roll = random.randrange(1, 7)
        return self._current_roll

    def current_turn(self) -> User:
        return self.players[self._current_turn]

    def to_dict(self):
        return {'name': self.name, 'players': [p.nickname for p in self.players], 'turn': self.current_turn().nickname,
                'player_positions': self.board.player_position}

    def move(self, position: Vector2d):
        if not self._rolled_dice:
            raise Exception('You must roll the dice before moving')
        if self._moved:
            raise Exception("You can't move twice in the same turn")

        self.board.move_player(position, self.current_turn().nickname, self._current_roll)
        self._moved = True
