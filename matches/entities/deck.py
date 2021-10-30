import random
from matches.match import Match
from .card import Card

class Deck:

    def __init__(self, match: Match) -> None:
        self.match = match

        # Define the deck
        self.cards = [
            Card(1, "Dracula"), Card(1, "Frankenstein"), Card(1, "Werewolf"),
            Card(1, "Ghost"), Card(1, "Mummy"), Card(1, "Dr. Jekyll and Mr Hyde"),
            Card(2, "Count"), Card(2, "Countess"), Card(2, "Housekeeper"),
            Card(2, "Butler"), Card(2, "Maid"), Card(2, "Gardener"),
            Card(3, "Bedroom"), Card(3, "Library"), Card(3, "Cellar"),
            Card(3, "Garage"), Card(3, "Laboratory"), Card(3, "Pantheon"),
            Card(3, "Lounge"), Card(3, "Lobby"), Card(4, "Salem Witch")
        ]

        # Define the mystery
        self.match.mystery = (random.choice(self.cards[0:6]),
                              random.choice(self.cards[6:12]),
                              random.choice(self.cards[12:20]))

        for card in self.match.mystery:
            self.cards.remove(card)

        # Shuffle the deck cards
        random.shuffle(self.cards)

    def deal_cards(self) -> None:
        n_players = len(self.match.players)
        for i in range (0,18):
            self.match.cards[i%n_players][1].append(self.cards[i])
