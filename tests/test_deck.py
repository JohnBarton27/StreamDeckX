import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from deck import Deck, XLDeck


class TestDeck(unittest.TestCase):

    def setUp(self):
        device_manager_patch = patch('deck.DeviceManager')
        m_dev_manager = device_manager_patch.start()
        self.addCleanup(device_manager_patch.stop)

        self.m_dev_manager = MagicMock()
        m_dev_manager.return_value = self.m_dev_manager

    def test_get_connected_single_xl(self):
        """Deck.get_connected.single_xl"""
        xl_deck1 = MagicMock()
        xl_deck1.deck_type.return_value = 'Stream Deck XL'
        xl_deck1.id.return_value = 'xl_deck1_id'
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

    @patch('deck.Deck._generate_buttons')
    def test_init(self, m_gen_buttons):
        """XLDeck.__init__"""
        deck = XLDeck('xl_id')
        self.assertEqual(deck.id, 'xl_id')
        self.assertEqual(deck.buttons, [])
        m_gen_buttons.assert_called()

    def test_generate_buttons(self):
        """XLDeck._generate_buttons"""
        deck = XLDeck('xl_id')
        self.assertEqual(len(deck.buttons), 32)
        self.assertEqual(deck.buttons[0].position, 0)
        self.assertEqual(deck.buttons[12].position, 12)
        self.assertEqual(deck.buttons[31].position, 31)

    @patch('button.Button.html', new_callable=PropertyMock)
    def test_html(self, m_button_html):
        """XLDeck.html"""
        deck = XLDeck('xl_id')
        m_button_html.return_value = 'BUTTON_HTML'

        row = "BUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTML"

        self.assertEqual(deck.html, f"<br/>{row}<br/>{row}<br/>{row}<br/>{row}")


if __name__ == '__main__':
    unittest.main()
