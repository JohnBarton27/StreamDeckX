import unittest
from unittest.mock import patch, MagicMock

import streamdeckx


class TestStreamdeckX(unittest.TestCase):

    def setUp(self) -> None:
        get_conn_patch = patch('deck.Deck.get_connected')
        self.m_get_connected = get_conn_patch.start()
        self.addCleanup(get_conn_patch.stop)

    def test_get_connected_decks(self):
        deck1 = MagicMock()
        deck2 = MagicMock()

        self.m_get_connected.return_value = [deck1, deck2]

        decks = streamdeckx._get_connected_decks()

        self.assertEqual([deck1, deck2], decks)

    def test_get_deck_by_id(self):
        deck1 = MagicMock()
        deck1.id = 'def456'
        deck2 = MagicMock()
        deck2.id = 'abc123'

        self.m_get_connected.return_value = [deck1, deck2]

        deck = streamdeckx._get_deck_by_id('abc123')

        self.assertEqual(deck2, deck)

    def test_get_deck_by_id_no_match(self):
        deck1 = MagicMock()
        deck1.id = 'def456'
        deck2 = MagicMock()
        deck2.id = 'abc123'

        self.m_get_connected.return_value = [deck1, deck2]

        deck = streamdeckx._get_deck_by_id('john')

        self.assertIsNone(deck)


if __name__ == '__main__':
    unittest.main()
