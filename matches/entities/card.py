from enum import Enum

class CardType(Enum):

    MONSTER = "Monster"
    VICTIM = "Victim"
    ROOM = "Room"
    SALEM_WITCH = "Salem Witch"

class Card:

    def __init__(self, type: str, name: str) -> None:
        self.type = CardType(type)            
        self.name = name

    def __eq__(self, other) -> bool:
        return self.name == other.name
