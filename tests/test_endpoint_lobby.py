import requests
import unittest


class TestEndpointLobby(unittest.TestCase):
    url = "http://127.0.0.1:8000"
    

    def test_create_lobby(self):
        response = requests.post(self.url + "/create-lobby?name=lobby&host=host")

        self.assertEqual(response.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(response.json(), {'lobby': {
                                                    'name': 'lobby', 'host': 'host',
                                                    'current_players': 1,
                                                    'max_players': 6},
                                            'info': "Lobby was created"})
