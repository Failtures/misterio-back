import unittest
from util.vector import Vector2d
from matches.match import Match
from users.user import User


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('test_match', [User('user1'), User('user2')])

    def prepare_turn(self):
        dice_value = self.match.roll_dice()
        current_turn = self.match.current_turn()

        if current_turn.nickname != 'user1':
            self.match.next_turn()
            dice_value = self.match.roll_dice()

        return dice_value

    def test_moves_right_distance(self):
        dice_value = self.prepare_turn()
        start_pos_p1 = Vector2d(0, 6)

        new_pos = Vector2d(start_pos_p1.x + dice_value, start_pos_p1.y)

        # Raises exception if something goes wrong
        self.match.move(new_pos)

    def test_cannot_move_more_than_dice_roll(self):
        self.prepare_turn()

        try:
            # Can't roll a 7
            self.match.move(Vector2d(7, 6))
        except Exception:
            return
        self.assertTrue(False, 'Player moved more than 6 spaces')

    def test_cannot_move_twice(self):
        dice_roll = self.prepare_turn()

        try:
            self.match.move(Vector2d(1, 6))
            self.match.move(Vector2d(2, 6))
        except Exception:
            return
        self.assertTrue(False, 'Moved twice in the same turn')
