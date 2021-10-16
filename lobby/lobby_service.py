from typing import List
from users.user import User
from .lobby import Lobby


class LobbyService:

    def __init__(self):
        self.lobbies = []

    def create_new_lobby(self, lobby_name: str, host: str) -> None:
        #When you create your lobby, you have to provide your user name 
        host_user = User(host)
        # Defaults to player's nickname if no lobby name is provided
        if lobby_name is None or lobby_name == '':
            lobby_name = f"{host}'s lobby"

        self.lobbies.append(Lobby(lobby_name, host_user))

    def get_lobbies(self) -> List[Lobby]:
        return self.lobbies
