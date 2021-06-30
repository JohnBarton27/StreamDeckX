import unittest
from unittest.mock import patch, MagicMock

from streamdeckx.deck import Deck, XLDeck


class TestDeck(unittest.TestCase):

    def setUp(self):
        device_manager_patch = patch('streamdeckx.deck.DeviceManager')
        m_dev_manager = device_manager_patch.start()
        self.addCleanup(device_manager_patch.stop)

        self.m_dev_manager = MagicMock()
        m_dev_manager.return_value = self.m_dev_manager

    def test_get_connected_single_xl(self):
        """Deck.get_connected.single_xl"""
        xl_deck1 = MagicMock()
        xl_deck1.deck_type.return_value = 'Stream Deck XL'
        xl_deck1.id = 'xl_deck1_id'
        self.m_dev_manager.enumerate.return_value = [xl_deck1]
        
        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 1)
        self.assertEqual(type(decks[0]), XLDeck)
        self.assertEqual(decks[0].id, 'xl_deck1_id')

    @patch('builtins.print')
    def test_get_connected_unknown(self, m_print):
        """Deck.get_connected.unknown"""
        unknown_deck1 = MagicMock()
        unknown_deck1.deck_type.return_value = 'Stream Deck Unknown'
        unknown_deck1.id = 'unknown_deck1_id'
        dev_manager = MagicMock()
        self.m_dev_manager.enumerate.return_value = [unknown_deck1]

        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 0)
        m_print.assert_called()


class TestXLDeck(unittest.TestCase):
    def test_init(self):
        """XLDeck.__init__"""
        deck = XLDeck('xl_id')
        self.assertEqual(deck.id, 'xl_id')
        self.assertEqual(deck.buttons, [])


if __name__ == '__main__':
    unittest.main()
