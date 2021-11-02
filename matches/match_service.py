from typing import List
from users.user import User
from .match import Match
from .entities.deck import Deck


class MatchService:

    def __init__(self):
        self.matches = []

    def create_new_match(self, name: str, players: List[User]) -> Match:
        match = Match(name, players)

        deck = Deck(match)
        deck.deal_cards()

        self.matches.append(match)
        
        return match

    def get_matches(self) -> List[Match]:
        return self.matches

    def get_match_by_name(self, name) -> Match:
        return next(m for m in self.matches if m.name == name)

    def get_player_in_match(self, match: Match, player: str):
        return next(start_player for start_player in match.players if start_player.nickname == player)
