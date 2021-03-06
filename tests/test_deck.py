import unittest
from unittest.mock import call, patch, MagicMock, PropertyMock

from test_base import BaseStreamdeckXTest
from deck import Deck, MiniDeck, OriginalDeck, XLDeck


class TestDeck(BaseStreamdeckXTest):

    def setUp(self):
        patch_render_button = patch('button.Button.update_key_image')
        self.m_render_button = patch_render_button.start()
        self.addCleanup(patch_render_button.stop)

        device_manager_patch = patch('deck.DeviceManager')
        m_dev_manager = device_manager_patch.start()
        self.addCleanup(device_manager_patch.stop)

        self.m_dev_manager = MagicMock()
        m_dev_manager.return_value = self.m_dev_manager

        deck_dao_by_id_patch = patch('deck.DeckDao.get_by_id')
        self.m_deck_dao_by_id = deck_dao_by_id_patch.start()
        self.addCleanup(deck_dao_by_id_patch.stop)

        deck_dao_create_patch = patch('deck.DeckDao.create')
        self.m_deck_dao_create = deck_dao_create_patch.start()
        self.addCleanup(deck_dao_create_patch.stop)

    @patch('deck.Deck._get_serial_from_session_id')
    def test_deck_interface(self, m_from_session_id):
        """Deck.deck_interface"""
        deck_interface1 = MagicMock()
        deck_interface1.get_serial_number.return_value = 'def456'
        deck_interface1.id.return_value = 'deck1_id'

        deck_interface2 = MagicMock()
        deck_interface2.get_serial_number.return_value = 'abc123'
        deck_interface2.id.return_value = 'deck2_id'

        self.m_dev_manager.enumerate.return_value = [deck_interface1, deck_interface2]
        m_from_session_id.side_effect = ['def456', 'abc123']

        deck = XLDeck('abc123')

        self.assertEqual(deck.deck_interface, deck_interface2)
        m_from_session_id.assert_has_calls([call('deck1_id'), call('deck2_id')], any_order=False)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_open_from_closed(self, m_deck_int):
        """Deck.open.from_closed"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = False
        deck_interface.open.reset_mock()

        deck.open()

        self.assertEqual(deck_interface.open.call_count, 1)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_open_from_open(self, m_deck_int):
        """Deck.open.from_open"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = True
        deck_interface.open.reset_mock()

        deck.open()

        self.assertEqual(deck_interface.open.call_count, 0)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_close_from_closed(self, m_deck_int):
        """Deck.close.from_closed"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = False
        deck_interface.close.reset_mock()

        deck.close()

        self.assertEqual(deck_interface.close.call_count, 0)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_close_from_open(self, m_deck_int):
        """Deck.close.from_open"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = True
        deck_interface.close.reset_mock()

        deck.close()

        self.assertEqual(deck_interface.close.call_count, 1)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_reset_from_closed(self, m_deck_int):
        """Deck.reset.from_closed"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = False
        deck_interface.open.reset_mock()
        deck_interface.reset.reset_mock()
        deck_interface.close.reset_mock()

        deck.reset()

        self.assertEqual(deck_interface.open.call_count, 0)
        self.assertEqual(deck_interface.close.call_count, 0)
        self.assertEqual(deck_interface.reset.call_count, 1)

    @patch('deck.Deck.deck_interface', new_callable=PropertyMock)
    def test_reset_from_open(self, m_deck_int):
        """Deck.reset.from_open"""
        deck_interface = MagicMock()
        deck_interface.get_serial_number.return_value = 'abc123'

        m_deck_int.return_value = deck_interface

        self.m_dev_manager.enumerate.return_value = [deck_interface]

        deck = XLDeck('abc123')
        deck._is_open = True
        deck_interface.open.reset_mock()
        deck_interface.reset.reset_mock()
        deck_interface.close.reset_mock()

        deck.reset()

        self.assertEqual(deck_interface.open.call_count, 0)
        self.assertEqual(deck_interface.close.call_count, 0)
        self.assertEqual(deck_interface.reset.call_count, 1)

    @patch('deck.Deck._get_instantiated_deck_by_session_id')
    def test_get_connected_single_xl(self, m_inst_by_id):
        """Deck.get_connected.single_xl"""
        xl_deck1 = MagicMock()
        xl_deck1.deck_type.return_value = 'Stream Deck XL'
        xl_deck1.get_serial_number.return_value = 'xl_deck1_id'
        self.m_dev_manager.enumerate.return_value = [xl_deck1]
        self.m_deck_dao_by_id.return_value = None
        m_inst_by_id.return_value = None

        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 1)
        self.assertEqual(type(decks[0]), XLDeck)
        self.assertEqual(decks[0].id, 'xl_deck1_id')
        self.m_deck_dao_create.assert_called()

    @patch('deck.Deck._get_instantiated_deck_by_session_id')
    def test_get_connected_single_original(self, m_inst_by_id):
        """Deck.get_connected.single_original"""
        orig_deck1 = MagicMock()
        orig_deck1.deck_type.return_value = 'Stream Deck Original'
        orig_deck1.get_serial_number.return_value = 'orig_deck1'
        self.m_dev_manager.enumerate.return_value = [orig_deck1]
        self.m_deck_dao_by_id.return_value = None
        m_inst_by_id.return_value = None

        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 1)
        self.assertEqual(type(decks[0]), OriginalDeck)
        self.assertEqual(decks[0].id, 'orig_deck1')
        self.m_deck_dao_create.assert_called()

    @patch('deck.Deck._get_instantiated_deck_by_session_id')
    def test_get_connected_original_xl(self, m_inst_by_id):
        """Deck.get_connected.original_xl"""
        orig_deck1 = MagicMock()
        orig_deck1.deck_type.return_value = 'Stream Deck Original'
        orig_deck1.get_serial_number.return_value = 'orig_deck1'

        xl_deck1 = MagicMock()
        xl_deck1.deck_type.return_value = 'Stream Deck XL'
        xl_deck1.get_serial_number.return_value = 'xl_deck1_id'

        self.m_dev_manager.enumerate.return_value = [orig_deck1, xl_deck1]
        self.m_deck_dao_by_id.return_value = None
        m_inst_by_id.return_value = None

        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 2)
        self.assertEqual(type(decks[0]), OriginalDeck)
        self.assertEqual(type(decks[1]), XLDeck)
        self.assertEqual(decks[0].id, 'orig_deck1')
        self.assertEqual(decks[1].id, 'xl_deck1_id')
        self.m_deck_dao_create.assert_called()

    @patch('deck.Deck._get_instantiated_deck_by_session_id')
    @patch('builtins.print')
    def test_get_connected_unknown(self, m_print, m_inst_by_id):
        """Deck.get_connected.unknown"""
        unknown_deck1 = MagicMock()
        unknown_deck1.deck_type.return_value = 'Stream Deck Unknown'
        unknown_deck1.get_serial_number.return_value = 'unknown_deck1_id'
        dev_manager = MagicMock()
        self.m_dev_manager.enumerate.return_value = [unknown_deck1]
        self.m_deck_dao_by_id.return_value = None
        m_inst_by_id.return_value = None

        decks = Deck.get_connected()

        self.m_dev_manager.enumerate.assert_called()

        self.assertEqual(len(decks), 0)
        m_print.assert_called()
        self.m_deck_dao_create.assert_not_called()

    def test_get_instantiated_deck_by_session_id(self):
        """Deck.get_instantiated_deck_by_id"""
        deck1 = XLDeck('xl_id', session_id='1_sess')
        deck2 = OriginalDeck('orig_id1', session_id='2_sess')
        deck3 = OriginalDeck('orig_id2', session_id='3_sess')

        deck2_from_inst = Deck._get_instantiated_deck_by_session_id('2_sess')

        self.assertEqual(deck2_from_inst, deck2)


class TestXLDeck(unittest.TestCase):

    def setUp(self) -> None:
        patch_render_button = patch('button.Button.update_key_image')
        self.m_render_button = patch_render_button.start()
        self.addCleanup(patch_render_button.stop)

    def test_init(self):
        """XLDeck.__init__"""
        deck = XLDeck('xl_id')
        self.assertEqual(deck.id, 'xl_id')
        self.assertEqual(len(deck.buttons), 32)

    @patch('button.Button.html', new_callable=PropertyMock)
    def test_html(self, m_button_html):
        """XLDeck.html"""
        deck = XLDeck('xl_id')
        m_button_html.return_value = 'BUTTON_HTML'

        row = "BUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTMLBUTTON_HTML"

        self.assertEqual(deck.html, f"<br/>{row}<br/>{row}<br/>{row}<br/>{row}")


class TestOriginalDeck(unittest.TestCase):

    def setUp(self) -> None:
        patch_render_button = patch('button.Button.update_key_image')
        self.m_render_button = patch_render_button.start()
        self.addCleanup(patch_render_button.stop)

    def test_init(self):
        """OriginalDeck.__init__"""
        deck = OriginalDeck('orig_id')
        self.assertEqual(deck.id, 'orig_id')
        self.assertEqual(len(deck.buttons), 15)

    def test_str(self):
        """OriginalDeck.__str__"""
        deck = OriginalDeck('orig_id')

        self.assertEqual(str(deck), 'Stream Deck Original')

    def test_repr(self):
        """OriginalDeck.__repr__"""
        deck = OriginalDeck('orig_id')

        self.assertEqual(repr(deck), 'Stream Deck Original (orig_id)')

    @patch('button.Button.html', new_callable=PropertyMock)
    def test_html(self, m_button_html):
        """OriginalDeck.html"""
        deck = OriginalDeck('orig_id')
        m_button_html.return_value = '<BTN>'

        row = "<BTN><BTN><BTN><BTN><BTN>"

        self.assertEqual(deck.html, f"<br/>{row}<br/>{row}<br/>{row}")


class TestMiniDeck(unittest.TestCase):

    def setUp(self) -> None:
        patch_render_button = patch('button.Button.update_key_image')
        self.m_render_button = patch_render_button.start()
        self.addCleanup(patch_render_button.stop)

    def test_init(self):
        """MiniDeck.__init__"""
        deck = MiniDeck('mini_id')
        self.assertEqual(deck.id, 'mini_id')
        self.assertEqual(len(deck.buttons), 6)

    @patch('button.Button.html', new_callable=PropertyMock)
    def test_html(self, m_button_html):
        """MiniDeck.html"""
        deck = MiniDeck('mini_id')
        m_button_html.return_value = '<BTN>'

        row = "<BTN><BTN><BTN>"

        self.assertEqual(deck.html, f"<br/>{row}<br/>{row}")


if __name__ == '__main__':
    unittest.main()
