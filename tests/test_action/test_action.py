import unittest
from unittest.mock import MagicMock, patch

from test_base import BaseStreamdeckXTest

from action.action import DelayAction, ApplicationAction
from action.text_action import TextAction


class TestTextAction(BaseStreamdeckXTest):

    def test_init(self):
        """TextAction.__init__"""
        btn = MagicMock()
        action = TextAction('username', btn, 1)
        self.assertEqual(action.text, 'username')

    def test_repr(self):
        """TextAction.__repr__"""
        btn = MagicMock()
        action = TextAction('username', btn, 1)
        self.assertEqual(repr(action), 'username')

    def test_str(self):
        """TextAction.__str__"""
        btn = MagicMock()
        action = TextAction('username', btn, 1)
        self.assertEqual(str(action), 'username')

    def test_eq_equal(self):
        """TextAction.__eq__.equal"""
        btn = MagicMock()
        action1 = TextAction('username', btn, 1)
        action2 = TextAction('username', btn, 1)

        self.assertEqual(action1, action2)

    def test_eq_diff_types(self):
        """TextAction.__eq__.diff_types"""
        btn = MagicMock()
        action1 = TextAction('username', btn, 1)
        action2 = 'username'

        self.assertNotEqual(action1, action2)

    def test_eq_diff_text(self):
        """TextAction.__eq__.diff_text"""
        btn = MagicMock()
        action1 = TextAction('username', btn, 1)
        action2 = TextAction('password', btn, 1)

        self.assertNotEqual(action1, action2)

    def test_hash(self):
        """TextAction.__hash__"""
        btn = MagicMock()
        action = TextAction('username', btn, 1)
        self.assertEqual(hash(action), hash('username'))

    def test_display_value(self):
        btn = MagicMock()
        action = TextAction('username', btn, 1)
        self.assertEqual('username', action.display_value)


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


class TestApplicationAction(BaseStreamdeckXTest):

    def test_action_type(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 0)

        self.assertEqual('APPLICATION', action.action_type)

    def test_init(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 0)

        self.assertEqual('/home/john/my_app.sh', action.application)
        self.assertEqual(btn, action.button)

    def test_display_value(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 1)
        self.assertEqual('Open /home/john/my_app.sh', action.display_value)

    @patch('subprocess.call')
    def test_execute(self, m_sub_call):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 1)
        action.execute()

        m_sub_call.assert_called_with('/home/john/my_app.sh')


if __name__ == '__main__':
    unittest.main()
