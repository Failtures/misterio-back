from users.user import User
from .lobby import Lobby


class LobbyService:

    def __init__(self):
        self.lobbies = []

    def create_new_lobby(self, lobby_name: str, host: User) -> None:
        # Defaults to player's nickname if no lobby name is provided
        if lobby_name is None or lobby_name == '':
            lobby_name = f"{host.nickname}'s lobby"

        self.lobbies.append(Lobby(lobby_name, host))

    def get_lobbies(self) -> [Lobby]:
        return self.lobbies
