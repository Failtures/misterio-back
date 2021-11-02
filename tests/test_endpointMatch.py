from fastapi.testclient import TestClient
from .working_test_case import TestCaseFastAPI
from main import app
from extensions import matchservice


class TestMatchEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_end_turn(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-end-turn'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-end-turn'})
            #There are 2 receive per accion because there is one messege per player
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-end-turn'})
            websocket.receive_json()
            websocket.receive_json()

            for i in range(5):
                match = matchservice.get_match_by_name('test-end-turn')
                if(match.current_turn().nickname == 'host'):
                    websocket.send_json({'action': 'match_end_turn', 'match_name': 'test-end-turn'})
                    data = websocket.receive_json()
                    websocket.receive_json()
                    self.assertEqual(data, {'action': 'turn_passed', 'current_turn': 'test-player'})
                else: 
                    websocket.send_json({'action': 'match_end_turn', 'match_name': 'test-end-turn'})
                    data = websocket.receive_json()
                    websocket.receive_json()
                    self.assertEqual(data, {'action': 'turn_passed', 'current_turn': 'host'})