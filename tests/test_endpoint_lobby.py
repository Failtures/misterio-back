from fastapi.testclient import TestClient
from working_test_case import TestCaseFastAPI
from main import app


class TestLobbyEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def create_dummy_lobbies(self, quantity: int = 1):
        for i in range(quantity):
            self.client.post(f"/create-lobby?name=lobby{i}&host=host{i}")

    def test_create_lobby(self):
        res = self.client.post("/create-lobby?name=lobby&host=host")

        self.assertEqual(res.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(res.json(), {'lobby': {
            'name': 'lobby', 'host': 'host',
            'current_players': 1,
            'max_players': 6},
            'info': "Lobby was created"})

    def test_get_lobbies(self):
        self.create_dummy_lobbies(5)
        res = self.client.get('/get-lobbies')
        lobbies = res.json()['lobbies']

        self.assertEqual(res.status_code, 200)
        # Has to be six since previous test added one
        self.assertEqual(len(lobbies), 6)

    def test_join_when_full(self):
        # First, five players join the lobby0
        for i in range(5):
            self.client.put(f"/join-player?name=lobby0&player=player{i}")
        # Then an extra player joins the lobby
        res = self.client.put("/join-player?name=lobby0&player=player5")

        lobby = res.json()['lobby']

        self.assertEqual(res.status_code, 502, "The status code isn't correct (502)")
        self.assertEqual(lobby, None)

