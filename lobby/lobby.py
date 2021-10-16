from users.user import User


class Lobby:

    MIN_PLAYERS = 2
    MAX_PLAYERS = 6

    def __init__(self, name: str, host: User):
        self.name = name
        self.host = host
        self.players = [host]

    def join(self, user: User) -> None:
        if len(self.players) < 6:
            self.players.append(user)
        elif user in self.players:
            raise Exception('Player is already in the lobby')
        else:
            raise Exception('Lobby is full')

    def leave(self, user: User) -> None:
        if user == self.host:
            # If host leaves, kick all players
            self.players = []
        else:
            self.players.remove(user)

    def current_players(self) -> int:
        return len(self.players)

    def can_start(self, user: User) -> bool:
        return user == self.host and 2 < self.current_players() < 6

    def to_dict(self):
        return {'name': self.name, 'host': self.host.nickname,
                'current_players': self.current_players(),
                'max_players': self.MAX_PLAYERS}
