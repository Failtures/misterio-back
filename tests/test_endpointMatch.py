from fastapi.testclient import TestClient
from main import app
from extensions import matchservice
from tests.working_test_case import TestCaseFastAPI


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
            
            match = matchservice.get_match_by_name("test-use-witch")
            
            # host use salem witch or fail trying
            if match.player_has_witch("host"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")
            else:
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "MONSTER"})
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
            
            match = matchservice.get_match_by_name("test-use-witch-twice")
            
            if match.player_has_witch("host"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")

                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")    
            elif match.player_has_witch("test-player"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")

                websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")

    def test_no_player_use_witch(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-no-player'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-no-player'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-no-player'})
            websocket.receive_json()
            websocket.receive_json()

            websocket.send_json({'action': 'match_use_witch', 'player_name': 'no-player',
                                'match_name': 'test-no-player', 'card_type': "MONSTER"})
            data = websocket.receive_json()
            self.assertEqual(data['action'], "failed")

    def test_accuse_victory(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-victory'})
            websocket.receive_json()
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-victory', 'lobby_name': 'test-accuse-victory'})
                websocket2.receive_json()
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-victory'})
                websocket.receive_json()
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-victory')
                turn_player = match.current_turn()
                mystery = match.mystery
                if turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-victory', 
                                                    'monster': mystery[0].name, 'victim': mystery[1].name, 'room': mystery[2].name})
                    data = websocket.receive_json()
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-victory', 
                                                    'monster': mystery[0].name, 'victim': mystery[1].name, 'room': mystery[2].name})
                    data = websocket2.receive_json()
                
                self.assertEqual(data, {'action': 'game_over', 'winner': turn_player.nickname})

    def test_accuse_defead(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-defeat'})
            websocket.receive_json()
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-defeat', 'lobby_name': 'test-accuse-defeat'})
                websocket2.receive_json()
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-defeat'})
                websocket.receive_json()
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-defeat')
                turn_player = match.current_turn()
                mystery = match.mystery
                if turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-defeat', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                    data = websocket.receive_json()
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-defeat', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                    data = websocket2.receive_json()
                
                self.assertEqual(data, {'action': 'player_deleted', 'loser': turn_player.nickname})

    def test_accuse_no_turn(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-accuse-no-host'})
            websocket.receive_json() #Lobby creado correctamente
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-no-turn', 'lobby_name': 'test-accuse-accuse-no-host'})
                websocket2.receive_json() #Usuario se uno correctamente
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-accuse-no-host'})
                websocket.receive_json() #Partida empezada correctamente
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-accuse-no-host')
                turn_player = match.current_turn()
                if not turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-accuse-no-host', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})

                    data = websocket.receive_json()
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-accuse-no-host', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                    data = websocket2.receive_json()
                
                self.assertEqual(data, {'action': 'failed', 'info': "It's not your turn"})