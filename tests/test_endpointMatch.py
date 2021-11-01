from fastapi.testclient import TestClient
from working_test_case import TestCaseFastAPI
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

    def test_get_hand(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()
            websocket.receive_json()

            websocket.send_json({'action': 'match_get_hand', 'player_name': 'host', 'match_name': 'test-get-hand'})
            data = websocket.receive_json()

            self.assertEqual(data['action'], 'get_hand')
            self.assertEqual(len(data['hand']), 9)


    def test_use_witch(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'match_get_hand', 'player_name': 'host', 'match_name': 'test-use-witch'})
            websocket.receive_json()

            match = matchservice.get_match_by_name("test-use-witch")
            
            # host use salem witch or fail trying
            if match.player_has_witch("host"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "Monster"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")
            else:
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "Monster"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")

    def test_use_witch_twice(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'match_get_hand', 'player_name': 'host', 'match_name': 'test-use-witch-twice'})
            websocket.receive_json()

            match = matchservice.get_match_by_name("test-use-witch-twice")
            
            if match.player_has_witch("host"):
                print("Host")
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "Monster"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")

                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "Monster"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")    
            # TODO match.player_has_witch("test-player") doesn't works, idk :D   
            # elif match.player_has_witch("test-player"):
            #     print("Other")
            #     websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
            #                         'match_name': 'test-use-witch-twice', 'card_type': "Monster"})
            #     data = websocket.receive_json()
            #     self.assertEqual(data['card']['type'], "MONSTER")

            #     websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
            #                         'match_name': 'test-use-witch-twice', 'card_type': "Monster"})
            #     data = websocket.receive_json()
            #     self.assertEqual(data['action'], "failed")
