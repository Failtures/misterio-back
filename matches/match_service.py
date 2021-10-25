from typing import List
from users.user import User
from .match import Match
from lobby.lobby import Lobby


class MatchService:

    def __init__(self):
        self.matches = []

    def create_new_match(self, name: str, players: List[User]) -> Match:
        match = Match(name, players)
        self.matches.append(Match(name, players))

        return match

    def get_matches(self) -> List[Match]:
        return self.matches

    def get_match_by_name(self, name) -> Match:
        for match in self.matches:
            if match.name == name:
                return match
