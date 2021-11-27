import unittest
from unittest.mock import patch, MagicMock

from action import MultiKeyPressAction, TextAction
from test_base import BaseStreamdeckXTest
import streamdeckx
from button import Button
from deck import NoSuchDeckException


class TestStreamdeckX(BaseStreamdeckXTest):

    def setUp(self) -> None:
        get_conn_patch = patch('deck.Deck.get_connected')
        self.m_get_connected = get_conn_patch.start()
        self.addCleanup(get_conn_patch.stop)

        # Testing Flask App setup
        streamdeckx.app.testing = True
        self.app = streamdeckx.app.test_client()

        # render_template
        render_template_patch = patch('streamdeckx.render_template')
        self.m_render_template = render_template_patch.start()
        self.addCleanup(render_template_patch.stop)

        # logging - warning
        logging_warning_patch = patch('streamdeckx.logging.warning')
        self.m_log_warn = logging_warning_patch.start()
        self.addCleanup(logging_warning_patch.stop)

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

        self.assertRaises(NoSuchDeckException, streamdeckx._get_deck_by_id, 'john')
        self.m_log_warn.assert_not_called()

    def test_get_deck_by_id_no_match_no_exception(self):
        deck1 = MagicMock()
        deck1.id = 'def456'
        deck2 = MagicMock()
        deck2.id = 'abc123'

        self.m_get_connected.return_value = [deck1, deck2]

        response = streamdeckx._get_deck_by_id('john', raise_exception=False)
        self.assertIsNone(response)

        self.m_log_warn.assert_called()

    def test_index_with_deck(self):
        deck = MagicMock()
        deck.html = '<p>Deck HTML</p>'

        self.m_get_connected.return_value = [deck]
        self.m_render_template.return_value = b'INDEX HTML'

        response = self.app.get('/')

        self.assertEqual(b'INDEX HTML', response.data)

        self.m_get_connected.assert_called()
        self.m_render_template.assert_called_with('index.html', connected_decks=[deck], curr_deck_html='<p>Deck HTML</p>')

    def test_index_no_deck(self):
        self.m_get_connected.return_value = []
        self.m_render_template.return_value = b'INDEX HTML'

        response = self.app.get('/')

        self.assertEqual(b'INDEX HTML', response.data)

        self.m_get_connected.assert_called()
        self.m_render_template.assert_called_with('index.html', connected_decks=[], curr_deck_html='<p>No Stream Decks connected!</p>')

    def test_get_config_html_no_deck(self):
        deck1 = MagicMock()
        deck1.id = 'def456'
        deck2 = MagicMock()
        deck2.id = 'abc123'

        self.m_get_connected.return_value = [deck1, deck2]

        with self.assertRaises(NoSuchDeckException):
            response = self.app.get('/configHtml?deckId=ghi789&button=27')
            self.assertEqual(500, response._status_code)

    def test_get_config_html(self):
        deck1 = MagicMock()
        deck1.id = 'def456'
        deck2 = MagicMock()
        deck2.id = 'abc123'

        button0 = MagicMock()
        button1 = MagicMock()

        deck2.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1, deck2]
        html = 'BUTTON HTML'
        self.m_render_template.return_value = html

        response = self.app.get('/configHtml?deckId=abc123&button=1')

        self.assertEqual(html.encode('utf-8'), response.data)

        self.m_get_connected.assert_called()
        self.m_render_template.assert_called_with('configuration.html', button=button1)

    def test_set_button_config_no_deck(self):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        self.m_get_connected.return_value = [deck1]

        with self.assertRaises(NoSuchDeckException):
            response = self.app.post('/setButtonConfig', data={
                'deckId': 'def123',
                'button': '1',
                'buttonText': 'Hello',
                'backgroundColor': '#008080',
                'textColor': '#000000',
                'fontSize': '16'
            })

            self.assertEqual(500, response._status_code)

        self.m_get_connected.assert_called()

    @patch('button.Button.set_text')
    def test_set_button_config(self, m_btn_set_text):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        button0 = MagicMock()
        button1 = MagicMock()
        button_image = MagicMock()
        button_image.image_bytes = b'an image!'
        button1.button_image = button_image

        deck1.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1]

        response = self.app.post('/setButtonConfig', data={
            'deckId': 'abc123',
            'button': '1',
            'buttonText': 'Hello',
            'backgroundColor': '#008080',
            'textColor': '#000000',
            'fontSize': '24'
        })

        self.assertEqual(b'an image!', response.data)

        self.m_get_connected.assert_called()
        button1.set_text.assert_called_with('Hello')
        button1.set_colors.assert_called_with('#000000', '#008080')
        button1.set_font_size.assert_called_with(24)

    def test_set_button_action_no_deck(self):
        self.m_get_connected.return_value = []

        with self.assertRaises(NoSuchDeckException):
            response = self.app.post('/setButtonAction', data={
                'deckId': 'def123',
                'button': '1',
                'action_text': 'username',
                'type': 'TEXT'
            })

            self.assertEqual(500, response._status_code)

        self.m_get_connected.assert_called()

    @patch('dao.action_dao.ActionDao.create')
    def test_set_button_action_text(self, m_create_action):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        button0 = Button(0, deck1)
        button1 = Button(1, deck1)

        deck1.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1]

        self.app.post('/setButtonAction', data={
            'deckId': 'abc123',
            'button': '1',
            'action_text': 'username',
            'type': 'TEXT'
        })

        self.assertEqual(1, len(button1.actions))
        self.assertTrue(isinstance(button1.actions[0], TextAction))

        self.m_get_connected.assert_called()
        m_create_action.assert_called()

    @patch('dao.action_dao.ActionDao.create')
    def test_set_button_action_multikey(self, m_create_action):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        button0 = Button(0, deck1)
        button1 = Button(1, deck1)

        deck1.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1]

        self.app.post('/setButtonAction', data={
            'deckId': 'abc123',
            'button': '1',
            'action_text': 'CTRL;ALT;DEL',
            'type': 'MULTIKEY'
        })

        self.assertEqual(1, len(button1.actions))
        
        self.assertTrue(isinstance(button1.actions[0], MultiKeyPressAction))
        self.assertEqual('CTRL', button1.actions[0].keys[0].name)

        self.m_get_connected.assert_called()
        m_create_action.assert_called()

    def test_delete_button_action_no_deck(self):
        self.m_get_connected.return_value = []

        with self.assertRaises(NoSuchDeckException):
            response = self.app.delete('/setButtonAction', data={
                'deckId': 'def123',
                'button': '1',
                'action': '21'
            })

            self.assertEqual(500, response._status_code)

        self.m_get_connected.assert_called()

    @patch('dao.action_dao.ActionDao.delete')
    def test_delete_button_action(self, m_delete_action):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        button0 = Button(0, deck1)
        button1 = Button(1, deck1)

        action = MagicMock()
        action.id = 21
        button1.actions = [action]

        deck1.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1]
        html = 'BUTTON HTML'
        self.m_render_template.return_value = html

        self.app.delete('/setButtonAction', data={
            'deckId': 'abc123',
            'button': '1',
            'action': '21'
        })

        self.assertEqual(0, len(button1.actions))

        self.m_get_connected.assert_called()
        m_delete_action.assert_called()
        self.m_render_template.assert_called_with('configuration.html', button=button1)


if __name__ == '__main__':
    unittest.main()
