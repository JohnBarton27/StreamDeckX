import unittest
from unittest.mock import MagicMock, patch, PropertyMock

from button import Button
from deck import OriginalDeck


class TestButton(unittest.TestCase):

    def setUp(self) -> None:
        patch_render_button = patch('button.Button.update_key_image')
        self.m_render_button = patch_render_button.start()
        self.addCleanup(patch_render_button.stop)

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

    @patch('button.Button.image_bytes', new_callable=PropertyMock)
    def test_html(self, m_image_bytes):
        """Button.html"""
        img_bytes = MagicMock()
        img_bytes.decode.return_value = '123456'
        m_image_bytes.return_value = img_bytes

        button = Button(12, self.deck1)
        self.assertEqual(button.html, '<span id="12" class="btn" onclick="openConfig(12)"><img id="12-img" height="72" width="72" src="data:image/PNG;base64, 123456"></span>')
        img_bytes.decode.assert_called()

    @patch('button_style.ButtonStyle.serialize')
    def test_serialize(self, m_bs_serialize):
        """Button.serialize"""
        button = Button(10, self.deck1)
        m_bs_serialize.return_value = {'label': '10'}

        self.assertEqual(button.serialize(), {'position': 10, 'style': {'label': '10'}})
        m_bs_serialize.assert_called()


if __name__ == '__main__':
    unittest.main()
