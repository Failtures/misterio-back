import random
from typing import List
from users.user import User


class Match:

    def __init__(self, name: str, players: List[User]):
        self._currentturn = 0

        self.name = name
        self.players = players

        # Shuffle turn order
        random.shuffle(self.players)

    def __eq__ (self, other):
        return self.name == other.name

    def next_turn(self) -> User:
        self._currentturn += 1
        self._currentturn %= len(self.players)

        return self.current_turn()

    def roll_dice(self) -> int:
        return random.randrange(1, 7)

    def current_turn(self) -> User:
        return self.players[self._currentturn]

    def players_to_list(self):
        player_list = []
        for player in self.players:
            player_list.append(player.nickname)
        return player_list

    def to_dict(self):
        return {'name': self.name, 'players': self.players_to_list(), 'turn': self._currentturn}
