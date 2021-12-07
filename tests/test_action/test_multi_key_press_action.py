import unittest
from unittest.mock import patch, MagicMock, call

from test_base import BaseStreamdeckXTest

from action.multi_key_press_action import MultiKeyPressAction


class TestMultiKeyPressAction(BaseStreamdeckXTest):

    def test_action_type(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual('MULTIKEY', action.action_type)

    def test_init(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual(['CTRL', 'S'], action.key_presses)
        self.assertEqual(btn, action.button)

    def test_repr(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual('CTRL+S', repr(action))

    def test_str(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual('CTRL+S', str(action))

    def test_eq_equal(self):
        btn = MagicMock()
        action1 = MultiKeyPressAction('CTRL;S', btn, 0)
        action2 = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual(action1, action2)

    def test_eq_diff_types(self):
        btn = MagicMock()
        action1 = MultiKeyPressAction('CTRL;S', btn, 0)
        action2 = True

        self.assertNotEqual(action1, action2)

    def test_eq_diff_num_keys(self):
        btn = MagicMock()
        action1 = MultiKeyPressAction('CTRL;S', btn, 0)
        action2 = MultiKeyPressAction('CTRL;SHIFT;S', btn, 0)

        self.assertNotEqual(action1, action2)

    def test_eq_diff_keys(self):
        btn = MagicMock()
        action1 = MultiKeyPressAction('CTRL;ALT;S', btn, 0)
        action2 = MultiKeyPressAction('CTRL;SHIFT;S', btn, 0)

        self.assertNotEqual(action1, action2)

    def test_eq_diff_orders(self):
        btn = MagicMock()
        action1 = MultiKeyPressAction('CTRL;ALT;S', btn, 0)
        action2 = MultiKeyPressAction('ALT;CTRL;S', btn, 0)

        self.assertEqual(action1, action2)

    def test_hash(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        self.assertEqual(hash('CTRL+S'), hash(action))

    def test_display_value(self):
        btn = MagicMock()
        action = MultiKeyPressAction('CTRL;ALT;DEL', btn, 1)
        self.assertEqual('CTRL + ALT + DEL', action.display_value)

    @patch('action.multi_key_press_action.MultiKeyPressAction._get_key')
    def test_execute(self, m_get_key):
        btn = MagicMock()
        ctrl_key = MagicMock()
        s_key = MagicMock()

        manager = MagicMock()
        manager.attach_mock(ctrl_key, 'ctrl_key')
        manager.attach_mock(s_key, 's_key')

        m_get_key.side_effect = [ctrl_key, s_key]
        action = MultiKeyPressAction('CTRL;S', btn, 0)

        action.execute()

        expected_calls = [call.ctrl_key.press(), call.s_key.press(), call.s_key.release(), call.ctrl_key.release()]
        self.assertEqual(expected_calls, manager.mock_calls)


if __name__ == '__main__':
    unittest.main()
