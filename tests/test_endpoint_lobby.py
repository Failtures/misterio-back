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
        response = self.client.post("/create-lobby?name=lobby&host=host")

        self.assertEqual(response.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(response.json(), {'lobby': {
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
