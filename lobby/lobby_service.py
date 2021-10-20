from typing import List
from users.user import User
from .lobby import Lobby


class LobbyService:

    def __init__(self):
        self.lobbies = []

    def create_new_lobby(self, lobby_name: str, host: User) -> None:
        if not isinstance(host, User):
            raise Exception('Host should be of type User')

        # Defaults to player's nickname if no lobby name is provided
        if lobby_name is None or lobby_name == '':
            lobby_name = f"{host.nickname}'s lobby"

        self.lobbies.append(Lobby(lobby_name, host))
        # TODO add exception if a user is not passed

    def get_lobbies(self) -> List[Lobby]:
        return self.lobbies

    def get_lobby_by_name(self, name: str) -> Lobby:
        return next(lobby for lobby in self.lobbies if lobby.name == name)

    def join_player(self, lobby_name: str, player_name: str) -> None:
        new_player = User(player_name)

        lobby = self.get_lobby_by_name(lobby_name)
        lobby.join(new_player)
