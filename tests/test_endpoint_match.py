from fastapi.testclient import TestClient
from working_test_case import TestCaseFastAPI
from main import app
from extensions import matchservice

class TestMatchEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_pass_turn(self):
        # Create a lobby with 3 players and start the match
        self.client.post("/create-lobby?name=lobby12&host=host")
        self.client.put("/join-player?name=lobby12&player=player2")
        self.client.put("/join-player?name=lobby12&player=player3")
        self.client.post("/start-match?lobby=lobby12&player=host")

        res = self.client.put('/end-turn?name=lobby12')
        self.assertEqual(res.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(res.json()['current_turn'], 1, "The turn isn't correct")

        res = self.client.put('/end-turn?name=lobby12')
        self.assertEqual(res.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(res.json()['current_turn'], 2, "The turn isn't correct")

        res = self.client.put('/end-turn?name=lobby12')
        self.assertEqual(res.status_code, 200, "The status code isn't correct (200)")
        self.assertEqual(res.json()['current_turn'], 0, "The turn isn't correct")

    def test_roll_dice(self):
        dice_numbers = []
        for i in range(100):
            dice = self.client.get('/roll-dice?name=lobby12').json()['dice']
            if(not dice in dice_numbers):
                dice_numbers.append(dice)
            if(len(dice_numbers) == 6):
                self.assertTrue(True)
                return
        self.assertTrue(False)