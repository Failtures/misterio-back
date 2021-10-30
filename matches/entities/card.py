from enum import Enum

class CardType(Enum):

    MONSTER = 1
    VICTIM = 2
    ROOM = 3
    SALEM_WITCH = 4

class Card:

    def __init__(self, type: int, name: str) -> None:
        self.type = CardType(type)            
        self.name = name

    def __eq__(self, other) -> bool:
        return self.name == other.name
