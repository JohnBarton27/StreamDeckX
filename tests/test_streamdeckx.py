import unittest
from unittest.mock import patch, MagicMock

import streamdeckx
from deck import NoSuchDeckException


class TestStreamdeckX(unittest.TestCase):

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
                'buttonText': 'Hello'
            })

            self.assertEqual(500, response._status_code)

        self.m_get_connected.assert_called()

    @patch('button.Button.set_text')
    def test_set_button_config(self, m_btn_set_text):
        deck1 = MagicMock()
        deck1.id = 'abc123'

        button0 = MagicMock()
        button1 = MagicMock()
        button1.image_bytes = b'an image!'

        deck1.buttons = [button0, button1]

        self.m_get_connected.return_value = [deck1]

        response = self.app.post('/setButtonConfig', data={
            'deckId': 'abc123',
            'button': '1',
            'buttonText': 'Hello'
        })

        self.assertEqual(b'an image!', response.data)

        self.m_get_connected.assert_called()
        button1.set_text.assert_called_with('Hello')


if __name__ == '__main__':
    unittest.main()
