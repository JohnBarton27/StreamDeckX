import unittest
from unittest.mock import patch, MagicMock

from streamdeckx.deck import Deck, XLDeck


class TestDeck(unittest.TestCase):

    def setUp(self):
        enumerate_patch = patch('StreamDeck.DeviceManager.DeviceManager.enumerate')
        self.m_enumerate = enumerate_patch.start()
        self.addCleanup(enumerate_patch.stop)

    def test_get_connected_single_xl(self):
        """Deck.get_connected.single_xl"""
        xl_deck1 = MagicMock()
        xl_deck1.deck_type.return_value = 'Stream Deck XL'
        xl_deck1.id = 'xl_deck1_id'
        self.m_enumerate.return_value = [xl_deck1]
        
        decks = Deck.get_connected()

        self.m_enumerate.assert_called()

        self.assertEqual(len(decks), 1)
        self.assertEqual(type(decks[0]), XLDeck)
        self.assertEqual(decks[0].id, 'xl_deck1_id')

    @patch('builtins.print')
    def test_get_connected_unknown(self, m_print):
        """Deck.get_connected.unknown"""
        unknown_deck1 = MagicMock()
        unknown_deck1.deck_type.return_value = 'Stream Deck Unknown'
        unknown_deck1.id = 'unknown_deck1_id'
        self.m_enumerate.return_value = [unknown_deck1]

        decks = Deck.get_connected()

        self.m_enumerate.assert_called()

        self.assertEqual(len(decks), 0)
        m_print.assert_called()


class TestXLDeck(unittest.TestCase):
    def test_init(self):
        """XLDeck.__init__"""
        deck = XLDeck('xl_id')
        self.assertEqual(deck.id, 'xl_id')


if __name__ == '__main__':
    unittest.main()
