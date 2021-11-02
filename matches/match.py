import random

from typing import List
from matches.entities.card import Card
from users.user import User
from .board_ import Board
from util.vector import Vector2d
from .square import SquareType, Square


class Match:

    def __init__(self, name: str, players: List[User]):
        self._current_turn = 0
        self._rolled_dice = False
        self._moved = False
        self._current_roll = 0

        self.name = name
        self.players = players
        self.board = Board([p.nickname for p in players])
        self.trapped = []

        # Shuffle turn order
        random.shuffle(self.players)
        
        # self.cards is an array with the tuple (User, List [Cards]) 
        self.cards = []
        # For each player a tuple is created in self.cards
        for players in self.players:
            self.cards.append([])

        # self.mystery represents the envelope, will be a tuple (Card, Card, Card)
        self.mystery = None


    def __eq__(self, other):
        return self.name == other.name

    def next_turn(self) -> User:
        # Reset flags
        self._rolled_dice = False
        self._moved = False

        self.__pass_turn()

        # If trapped, skip turn
        if self.current_turn() in self.trapped:
            self.trapped.remove(self.current_turn())
            self.__pass_turn()

        return self.current_turn()

    def __pass_turn(self):
        self._current_turn += 1
        self._current_turn %= len(self.players)

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
                'player_position': self.board.positions_to_dict()}

    def move(self, position: Vector2d) -> Square:
        prev_square = self.board.get_player_square(self.current_turn().nickname)

        if not self._rolled_dice:
            raise Exception('You must roll the dice before moving')
        if self._moved:
            raise Exception("You can't move twice in the same turn")

        square = self.board.move_player(position, self.current_turn().nickname, self._current_roll)
        self._moved = True

        if square.squaretype == SquareType.TRAP and prev_square.squaretype != SquareType.TRAP:
            self.trapped.append(self.current_turn())

        return square


    def get_hand(self, player: str) -> List[Card]:
        for i in range(0, len(self.players)):
            if self.players[i].nickname == player:
                return self.cards[i]
        raise Exception("Player doesn't exist in match")

    # Return true if player has the salem witch in hand
    def player_has_witch(self, player: str) -> bool:
        try:
            hand = self.get_hand(player)
            return any(c.name == "Salem Witch" for c in hand)
        except Exception:
            raise Exception("Player doesn't exist in match")

    # Delete the witch of salem from the player's hand
    def delete_witch(self, player) -> None:
        try:
            hand = self.get_hand(player)
            for i in range(0, len(hand)):
                if hand[i].name == "Salem Witch":
                    hand.pop(i)
                    return
        except Exception:
            raise Exception("Player doesn't exist in match")
