from fastapi.testclient import TestClient
from tests.working_test_case import TestCaseFastAPI
from main import app


class TestEndpointBoard(TestCaseFastAPI):

    def setUp(self) -> None:
        from extensions import matchservice;matchservice.matches = []
        self.client = TestClient(app)

    def test_move(self):
        failed = False
        with self.client.websocket_connect('/ws') as websocket2:
            websocket2.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'lobby'})
            websocket2.receive_json()

            with self.client.websocket_connect('/ws') as websocket:
                websocket.send_json({'action': 'lobby_join', 'player_name': 'player2', 'lobby_name': 'lobby'})
                websocket2.receive_json()
                websocket.receive_json()

                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'lobby'})
                turn = websocket.receive_json()

                if turn['match']['turn'] == 'player2':
                    websocket2.send_json({'action': 'match_roll_dice', 'match_name': 'lobby'})
                    websocket2.send_json({'action': 'match_move', 'match_name': 'lobby', 'pos_x': 6, 'pos_y': 1})
                    websocket2.send_json({'action': 'match_end_turn', 'player_name': 'host', 'match_name': 'lobby'})
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()


                websocket.send_json({'action': 'match_roll_dice', 'match_name': 'lobby'})
                dice = websocket.receive_json()

                websocket.send_json({'action': 'match_move', 'match_name': 'lobby', 'pos_x': 1, 'pos_y': 6})
                json = websocket.receive_json()

                self.assertEqual(json['square'], 'Regular')
