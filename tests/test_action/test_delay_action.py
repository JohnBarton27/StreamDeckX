import unittest
from unittest.mock import MagicMock

from test_base import BaseStreamdeckXTest

from action.delay_action import DelayAction


class TestDelayAction(BaseStreamdeckXTest):

    def test_action_type(self):
        btn = MagicMock()
        action = DelayAction('5', btn, 0)

        self.assertEqual('DELAY', action.action_type)

    def test_init(self):
        btn = MagicMock()
        action = DelayAction('5', btn, 0)

        self.assertEqual(5, action.delay_time)
        self.assertEqual(btn, action.button)

    def test_display_value(self):
        btn = MagicMock()
        action = DelayAction('10', btn, 1)
        self.assertEqual('10 seconds', action.display_value)


if __name__ == '__main__':
    unittest.main()
