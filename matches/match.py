import random
from typing import List
from users.user import User
from .board_ import Board
from util.vector import Vector2d


class Match:

    def __init__(self, name: str, players: List[User]):
        self._currentturn = 0
        self._rolleddice = False
        self._currentroll = 0

        self.name = name
        self.players = players
        self.board = Board([p.nickname for p in players])

        # Shuffle turn order
        random.shuffle(self.players)

    def __eq__ (self, other):
        return self.name == other.name

    def next_turn(self) -> User:
        self._currentturn += 1
        self._currentturn %= len(self.players)
        self._rolleddice = False

        return self.current_turn()

    def roll_dice(self) -> int:
        if self._rolleddice:
            raise Exception('Already rolled dice this turn')
        self._rolleddice = True
        self._currentroll = random.randrange(1, 7)
        return self._currentroll

    def current_turn(self) -> User:
        return self.players[self._currentturn]

    def to_dict(self):
        return {'name': self.name, 'players': [p.nickname for p in self.players], 'turn': self.current_turn().nickname,
                'player_positions': self.board.players}

    def move(self, position: Vector2d):
        player = self.current_turn()
        currentpos = self.board.get_player_position(player.nickname)
        distance = currentpos.distance_to(position)

        if self._rolleddice and distance > self._currentroll:
            raise Exception("Can't move more spaces than the dice roll value")

        self.board.move_player(position, self.current_turn().nickname)
