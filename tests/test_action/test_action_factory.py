import unittest

from test_base import BaseStreamdeckXTest

from action.action import MultiKeyPressAction, DelayAction
from action.action_factory import ActionFactory
from action.text_action import TextAction


class TestActionFactory(BaseStreamdeckXTest):

    def test_get_by_type_text(self):
        text = ActionFactory.get_by_type('TEXT')
        self.assertEqual(TextAction, text)

    def test_get_by_type_multikey(self):
        multikey = ActionFactory.get_by_type('MULTIKEY')
        self.assertEqual(MultiKeyPressAction, multikey)

    def test_get_by_type_delay(self):
        delay = ActionFactory.get_by_type('DELAY')
        self.assertEqual(DelayAction, delay)


if __name__ == '__main__':
    unittest.main()
