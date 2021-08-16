import unittest

from button import Button
from deck import OriginalDeck


class TestButton(unittest.TestCase):

    def setUp(self) -> None:
        self.deck1 = OriginalDeck('deck123')

    def test_init(self):
        """Button.__init__"""
        button = Button(12, self.deck1)
        self.assertEqual(button.position, 12)

    def test_repr(self):
        """Button.__repr__"""
        button = Button(12, self.deck1)
        self.assertEqual(repr(button), '12')

    def test_str(self):
        """Button.__str__"""
        button = Button(12, self.deck1)
        self.assertEqual(str(button), '12')

    def test_eq_equal(self):
        """Button.__eq__.equal"""
        button1 = Button(12, self.deck1)
        button2 = Button(12, self.deck1)
        self.assertEqual(button1, button2)

    def test_eq_diff_positions(self):
        """Button.__eq__.diff_positions"""
        button1 = Button(12, self.deck1)
        button2 = Button(14, self.deck1)
        self.assertNotEqual(button1, button2)

    def test_hash(self):
        """Button.__hash__"""
        button = Button(12, self.deck1)
        self.assertEqual(hash(button), hash(12))

    def test_html(self):
        """Button.html"""
        button = Button(12, self.deck1)
        self.assertEqual(button.html, '<span id="12" class="btn" onclick="openConfig(12)"></span>')

    def test_serialize(self):
        """Button.serialize"""
        button = Button(10, self.deck1)
        self.assertEqual(button.serialize(), {'position': 10})


if __name__ == '__main__':
    unittest.main()
