import unittest
from matches.match import Match
from users.user import User

class TestMatch2Players(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('testmatch', [User("host"), User("user1")])

    def test_correct_turns(self):
        turns = self.match.players
        self.assertTrue(turns[1] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")

        self.assertTrue(turns[0] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")


class TestMatch6Players(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('testmatch', [User("host"), User("user1"),
                                        User("user2"), User("user3"),
                                        User("user4"), User("user5"),])

    def test_correct_turns(self):
        turns = self.match.players
        self.assertTrue(turns[1] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.assertTrue(turns[2] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.assertTrue(turns[3] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.assertTrue(turns[4] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.assertTrue(turns[5] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.assertTrue(turns[0] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")