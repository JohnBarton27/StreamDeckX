import unittest
from unittest.mock import patch, MagicMock

from test_base import BaseStreamdeckXTest
from button_image import ButtonImage, ImageLine


class TestButtonImage(BaseStreamdeckXTest):

    def setUp(self) -> None:
        get_text_dimensions_patch = patch('button_image.ButtonImage.get_text_dimensions')
        self.m_get_text_dimensions = get_text_dimensions_patch.start()
        self.addCleanup(get_text_dimensions_patch.stop)
        self.m_get_text_dimensions.side_effect = get_text_dimensions_side_effect

    def test_init(self):
        style = MagicMock()
        deck = MagicMock()

        image = ButtonImage(style, deck)

        self.assertEqual(style, image.style)
        self.assertEqual(deck, image.deck)
        self.assertEqual(0, image._image_size)

    @patch('button_image.ButtonImage.draw_text')
    @patch('PIL.Image.new')
    @patch('PIL.Image.open')
    @patch('PIL.ImageDraw.Draw')
    @patch('StreamDeck.ImageHelpers.PILHelper.create_scaled_image')
    def test_image_with_icon(self, m_scaled_image, m_image_draw, m_image_open, m_image_new, m_draw_text):
        style = MagicMock()
        style.icon_path = 'image.png'
        deck = MagicMock()
        interface = MagicMock()
        deck.deck_interface = interface

        m_icon = MagicMock()
        m_image_open.return_value = m_icon

        m_image = MagicMock()
        m_image.size = (100, 50)
        m_scaled_image.return_value = m_image

        image = ButtonImage(style, deck)

        result = image.image
        self.assertEquals(m_image, result)
        self.assertEquals(100, image._image_size)

        m_scaled_image.assert_called_with(interface, m_icon, margins=[0, 0, 0, 0])
        m_image_open.assert_called_with('image.png')
        m_image_new.assert_not_called()
        m_image_draw.assert_called_with(m_image)
        m_draw_text.assert_called_with(m_image_draw.return_value)

    @patch('button_image.ButtonImage.draw_text')
    @patch('PIL.Image.new')
    @patch('PIL.Image.open')
    @patch('PIL.ImageDraw.Draw')
    @patch('StreamDeck.ImageHelpers.PILHelper.create_scaled_image')
    def test_image_without_icon(self, m_scaled_image, m_image_draw, m_image_open, m_image_new, m_draw_text):
        style = MagicMock()
        style.icon_path = ''
        style.rgb_background_color = '#008080'
        deck = MagicMock()
        interface = MagicMock()
        deck.deck_interface = interface

        m_icon = MagicMock()
        m_image_new.return_value = m_icon

        m_image = MagicMock()
        m_image.size = (100, 50)
        m_scaled_image.return_value = m_image

        image = ButtonImage(style, deck)

        result = image.image
        self.assertEquals(m_image, result)
        self.assertEquals(100, image._image_size)

        m_scaled_image.assert_called_with(interface, m_icon, margins=[0, 0, 0, 0])
        m_image_new.assert_called_with('RGB', (100, 100), '#008080')
        m_image_open.assert_not_called()
        m_image_draw.assert_called_with(m_image)
        m_draw_text.assert_called_with(m_image_draw.return_value)

    def test_get_max_width_single(self):
        font = MagicMock()

        text_lines = ['abc123']
        max_width = ButtonImage.get_max_width(text_lines, font)

        self.assertEqual(max_width, 6)

    def test_get_max_width_multiple(self):
        font = MagicMock()

        text_lines = ['abc123', 'a', '456']
        max_width = ButtonImage.get_max_width(text_lines, font)

        self.assertEqual(max_width, 6)

    def test_get_max_width_multiple_in_middle(self):
        font = MagicMock()

        text_lines = ['abc123', 'abcdef1234', '456']
        max_width = ButtonImage.get_max_width(text_lines, font)

        self.assertEqual(max_width, 10)

    def test_get_split_text_no_split(self):
        font = MagicMock()
        style = MagicMock()
        style.label = 'abc'
        deck = MagicMock()

        bi = ButtonImage(style, deck)
        bi._image_size = 10

        split_text = bi.get_split_text(font)

        self.assertEqual(['abc'], split_text)

    def test_get_split_text_single_split(self):
        font = MagicMock()
        style = MagicMock()
        style.label = 'abc 12345678'
        deck = MagicMock()

        bi = ButtonImage(style, deck)
        bi._image_size = 10

        split_text = bi.get_split_text(font)

        self.assertEqual(['abc', '12345678'], split_text)

    def test_get_split_text_multi_split(self):
        font = MagicMock()
        style = MagicMock()
        style.label = 'abc 123 45678 a'
        deck = MagicMock()

        bi = ButtonImage(style, deck)
        bi._image_size = 10

        split_text = bi.get_split_text(font)

        self.assertEqual(['abc 123', '45678 a'], split_text)


class TestImageLine(unittest.TestCase):

    def setUp(self) -> None:
        get_text_dimensions_patch = patch('button_image.ButtonImage.get_text_dimensions')
        self.m_get_text_dimensions = get_text_dimensions_patch.start()
        self.addCleanup(get_text_dimensions_patch.stop)
        self.m_get_text_dimensions.side_effect = get_text_dimensions_side_effect

    def test_repr(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)

        self.assertEqual('a line', repr(il))

    def test_str(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)

        self.assertEqual('a line', str(il))

    def test_width(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)

        self.assertEqual(il.width, 6)

        self.m_get_text_dimensions.assert_called_with('a line', font)

    def test_staged_width(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)
        il.stage_word('text')

        self.assertEqual(il.staged_width, 11)

        self.m_get_text_dimensions.assert_called_with('a line text', font)

    def test_stage_word(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)

        self.assertIsNone(il._staged_word)

        il.stage_word('for')

        self.assertEqual('for', il._staged_word)

    def test_commit_staged_word(self):
        font = MagicMock()
        il = ImageLine(['a', 'line'], font)
        il.stage_word('for')
        il.commit_staged_word()

        self.assertEqual(['a', 'line', 'for'], il.words)


def get_text_dimensions_side_effect(line, font):
    # This just returns the 'length' (number of characters) of the string to make testing easier
    return len(line), 0


if __name__ == '__main__':
    unittest.main()
