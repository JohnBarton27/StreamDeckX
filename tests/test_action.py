import unittest

from action import TextAction


class TestTextAction(unittest.TestCase):

    def test_init(self):
        """TextAction.__init__"""
        action = TextAction('username')
        self.assertEqual(action.text, 'username')

    def test_repr(self):
        """TextAction.__repr__"""
        action = TextAction('username')
        self.assertEqual(repr(action), 'username')

    def test_str(self):
        """TextAction.__str__"""
        action = TextAction('username')
        self.assertEqual(str(action), 'username')

    def test_eq_equal(self):
        """TextAction.__eq__.equal"""
        action1 = TextAction('username')
        action2 = TextAction('username')

        self.assertEqual(action1, action2)

    def test_eq_diff_types(self):
        """TextAction.__eq__.diff_types"""
        action1 = TextAction('username')
        action2 = 'username'

        self.assertNotEqual(action1, action2)

    def test_eq_diff_text(self):
        """TextAction.__eq__.diff_text"""
        action1 = TextAction('username')
        action2 = TextAction('password')

        self.assertNotEqual(action1, action2)

    def test_hash(self):
        """TextAction.__hash__"""
        action = TextAction('username')
        self.assertEqual(hash(action), hash('username'))


if __name__ == '__main__':
    unittest.main()
