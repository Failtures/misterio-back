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
        
        # self.cards is an array with the tuple (User, List [Cards]) 
        self.cards = []
        # For each player a tuple is created in self.cards
        for players in self.players:
            self.cards.append((players, []))

        # self.mystery represents the envelope, will be a tuple (Card, Card, Card)
        self.mystery = None


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

    def to_dict(self):
        return {'name': self.name, 'players': [p.nickname for p in self.players], 'turn': self._currentturn}
