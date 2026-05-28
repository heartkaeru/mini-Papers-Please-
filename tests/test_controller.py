import unittest

import config
from controller import GameController
from model import Decision, RoundResult


class GameControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = GameController.__new__(GameController)

    def test_fix_bool_returns_default_for_wrong_type(self):
        result = self.controller.fix_bool("yes", False)

        self.assertFalse(result)

    def test_fix_volume_limits_big_value(self):
        result = self.controller.fix_volume(2.5, config.DEFAULT_MUSIC_VOLUME)

        self.assertEqual(result, config.MAX_VOLUME)

    def test_fix_volume_limits_small_value(self):
        result = self.controller.fix_volume(-1, config.DEFAULT_MUSIC_VOLUME)

        self.assertEqual(result, config.MIN_VOLUME)

    def test_fix_volume_ignores_bool(self):
        result = self.controller.fix_volume(True, config.DEFAULT_MUSIC_VOLUME)

        self.assertEqual(result, config.DEFAULT_MUSIC_VOLUME)

    def test_fix_window_mode_number_returns_default_for_wrong_number(self):
        result = self.controller.fix_window_mode_number(100)

        self.assertEqual(result, config.DEFAULT_WINDOW_MODE_NUMBER)

    def test_result_text_for_correct_decision(self):
        result = RoundResult(
            player_decision=Decision.ALLOW,
            correct_decision=Decision.ALLOW,
            is_correct=True,
            errors=(),
            money_delta=10,
            balance=10,
            game_over=False,
        )

        text = self.controller.get_result_text(result)

        self.assertEqual(text, config.RESULT_CORRECT_TEXT.format(money_delta=10))

    def test_result_text_for_mistake(self):
        result = RoundResult(
            player_decision=Decision.ALLOW,
            correct_decision=Decision.DENY,
            is_correct=False,
            errors=(),
            money_delta=-5,
            balance=-5,
            game_over=False,
        )

        text = self.controller.get_result_text(result)

        self.assertEqual(text, config.RESULT_MISTAKE_TEXT.format(money_delta=-5))


if __name__ == "__main__":
    unittest.main()
