from typing import List
from users.user import User
from .match import Match
from lobby.lobby import Lobby

class MatchService:

    def __init__(self):
        self.matches = []

    def create_new_match(self, name: str, players: list[User] ) -> None:
        self.matches.append(Match(name, players))

    def get_matches(self) -> List[Match]:
        return self.matches

    def get_match_by_name(self, name):
        for match in self.matches:
            if match.name == name:
                return match



    
