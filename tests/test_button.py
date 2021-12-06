import unittest
from unittest.mock import MagicMock, patch, PropertyMock

from button import Button
from deck import OriginalDeck
from test_base import BaseStreamdeckXTest


class TestButton(BaseStreamdeckXTest):

    def setUp(self) -> None:
        self.deck1 = OriginalDeck('deck123')

        patch_action_execute = patch('action.action.Action.execute')
        self.m_action_exec = patch_action_execute.start()
        self.addCleanup(patch_action_execute.stop)

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

    @patch('button_image.ButtonImage.image_bytes', new_callable=PropertyMock)
    def test_html(self, m_image_bytes):
        """Button.html"""
        img_bytes = MagicMock()
        img_bytes.decode.return_value = '123456'
        m_image_bytes.return_value = img_bytes

        button = Button(12, self.deck1)
        self.assertEqual(button.html, '<span id="12" class="btn" onclick="openConfig(12)"><img id="12-img" height="72" width="72" src="data:image/PNG;base64, 123456"></span>')
        img_bytes.decode.assert_called()

    @patch('button.Button.button_dao.update')
    @patch('button.Button.update_key_image')
    def test_set_text(self, m_update_key_image, m_btn_update):
        button = Button(12, self.deck1)

        button.set_text('hello!')

        self.assertEqual('hello!', button.style.label)

        m_update_key_image.assert_called()
        m_btn_update.assert_called()

    @patch('button.Button.button_dao.update')
    @patch('button.Button.update_key_image')
    def test_set_colors(self, m_update_key_image, m_btn_update):
        button = Button(12, self.deck1)

        button.set_colors('#123456', '#abcdef')

        self.assertEqual('#123456', button.style.text_color)
        self.assertEqual('#abcdef', button.style.background_color)

        m_update_key_image.assert_called()
        m_btn_update.assert_called()

    @patch('button.Button.button_dao.update')
    @patch('button.Button.update_key_image')
    def test_set_font_size(self, m_update_key_image, m_btn_update):
        button = Button(12, self.deck1)

        button.set_font_size(200)

        self.assertEqual(200, button.style.font_size)

        m_update_key_image.assert_called()
        m_btn_update.assert_called()

    @patch('button.Button.button_dao.update')
    @patch('button.Button.update_key_image')
    def test_set_background_image(self, m_update_key_image, m_btn_update):
        button = Button(12, self.deck1)

        button.set_background_image('123ZZZ')

        self.assertEqual('123ZZZ', button.style.background_image)

        m_update_key_image.assert_called()
        m_btn_update.assert_called_with(button)

    def test_add_action(self):
        button = Button(12, self.deck1)

        self.assertEqual([], button.actions)

        action1 = MagicMock()
        action2 = MagicMock()

        button.add_action(action1)
        self.assertEquals([action1], button.actions)

        button.add_action(action2)
        self.assertEquals([action1, action2], button.actions)

    def test_add_action_duplicates(self):
        button = Button(12, self.deck1)

        self.assertEqual([], button.actions)

        action1 = MagicMock()

        button.add_action(action1)
        self.assertEquals([action1], button.actions)

        button.add_action(action1)
        self.assertEquals([action1, action1], button.actions)

    def test_execute_actions_none(self):
        button = Button(12, self.deck1)
        self.assertEqual([], button.actions)

        button.execute_actions()
        self.m_action_exec.assert_not_called()

    def test_execute_actions(self):
        button = Button(12, self.deck1)
        self.assertEqual([], button.actions)

        action1 = MagicMock()
        action2 = MagicMock()

        button.add_action(action1)
        button.add_action(action2)

        button.execute_actions()

        action1.execute.assert_called()
        action2.execute.assert_called()

    @patch('button_style.ButtonStyle.serialize')
    def test_serialize(self, m_bs_serialize):
        """Button.serialize"""
        button = Button(10, self.deck1)
        m_bs_serialize.return_value = {'label': '10'}

        self.assertEqual(button.serialize(), {'position': 10, 'style': {'label': '10'}})
        m_bs_serialize.assert_called()

    @patch('deck.Deck.deck_interface')
    @patch('button_image.ButtonImage.render_key_image')
    def test_update_key_image(self, m_render_key, m_deck_int):
        button = Button(10, self.deck1)
        image = MagicMock()
        m_render_key.return_value = image

        button.update_key_image()

        m_render_key.assert_called()
        m_deck_int.set_key_image.assert_called_with(10, image)


if __name__ == '__main__':
    unittest.main()
