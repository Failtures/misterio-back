from fastapi.testclient import TestClient
from working_test_case import TestCaseFastAPI
from main import app


class TestLobbyEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def create_dummy_lobbies(self, quantity: int = 1):
        with self.client.websocket_connect('/ws') as websocket:
            for i in range(quantity):
                lobby = ['test-lobby1','test-lobby2','test-lobby3','test-lobby4','test-lobby5']
                websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': lobby[i]})

    def test_get_lobbies(self):
        self.create_dummy_lobbies(5)
        res = self.client.get('/get-lobbies')
        lobbies = res.json()['lobbies']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(lobbies), 5)
        
    def test_join_lobby(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player1', 'lobby_name': 'test-lobby1'})
            data = websocket.receive_json()
            self.assertEqual(data,{'action': 'joined_lobby', 'lobby': {'current_players': 2,
                                                                    'host': 'host',
                                                                    'name': 'test-lobby1',
                                                                    'players': ['host', 'test-player1']}})
            

    def test_start_match_with(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-lobby2'})
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-lobby2'})
            data = websocket.receive_json()
            data = websocket.receive_json()
            data['match']['players'].sort()
            self.assertEqual(data, {'action': 'match_started', 'match': {'name': 'test-lobby2',
                                                                    'players': ['host', 'test-player'],
                                                                    'turn': 0}})

    def test_start_match_no_host(self):
        with self.client.websocket_connect('/ws') as websocket:  
            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-lobby3'})
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'test-player', 'lobby_name': 'test-lobby3'})
            websocket.receive_json()
            data = websocket.receive_json()
            self.assertEqual(data['action'], 'failed')

    def test_start_match_one_player(self):
        with self.client.websocket_connect('/ws') as websocket:  
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-one-player'})
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-one-player'})
            websocket.receive_json()
            data = websocket.receive_json()
            self.assertEqual(data['action'], 'failed')

    def test_leave_lobby(self):
        with self.client.websocket_connect('/ws') as websocket: 
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-leave-lobby'})
            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-leave-lobby'})
            websocket.send_json({'action': 'lobby_leave', 'player_name': 'test-player', 'lobby_name': 'test-leave-lobby'})
            for i in range(3):
                websocket.receive_json()
            data = websocket.receive_json()
            self.assertEqual(data,{'action': 'player_leaved', 'player_name': 'test-player'})

    def test_leave_lobby_host(self):
        with self.client.websocket_connect('/ws') as websocket: 
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-leave-host'})
            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-leave-host'})
            websocket.send_json({'action': 'lobby_leave', 'player_name': 'host', 'lobby_name': 'test-leave-host'})
            for i in range(3):
                websocket.receive_json()
            data = websocket.receive_json()
            self.assertEqual(data,{'action': 'lobby_removed', 'lobby_name': 'test-leave-host'})

    def test_leave_no_lobby(self):
        with self.client.websocket_connect('/ws') as websocket: 
            websocket.send_json({'action': 'lobby_leave', 'player_name': 'player', 'lobby_name': 'test-leave-no-lobby'})
            data = websocket.receive_json()
            self.assertEqual(data['action'],'failed')
    