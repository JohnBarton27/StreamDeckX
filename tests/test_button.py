import unittest

from streamdeckx.button import Button


class TestButton(unittest.TestCase):
    def test_init(self):
        """Button.__init__"""
        button = Button(12)
        self.assertEqual(button.position, 12)

    def test_repr(self):
        """Button.__repr__"""
        button = Button(12)
        self.assertEqual(repr(button), '12')

    def test_str(self):
        """Button.__str__"""
        button = Button(12)
        self.assertEqual(str(button), '12')

    def test_eq_equal(self):
        """Button.__eq__.equal"""
        button1 = Button(12)
        button2 = Button(12)
        self.assertEqual(button1, button2)

    def test_eq_diff_positions(self):
        """Button.__eq__.diff_positions"""
        button1 = Button(12)
        button2 = Button(14)
        self.assertNotEqual(button1, button2)

    def test_hash(self):
        """Button.__hash__"""
        button = Button(12)
        self.assertEqual(hash(button), hash(12))


if __name__ == '__main__':
    unittest.main()
