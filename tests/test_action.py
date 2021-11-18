import unittest
from unittest.mock import MagicMock

from action import TextAction, MultiKeyPressAction


class TestTextAction(unittest.TestCase):

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


class TestMultiKeyPressAction(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
