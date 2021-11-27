import unittest
from unittest.mock import patch

from test_base import BaseStreamdeckXTest
from button_style import ButtonStyle


class TestButtonStyle(BaseStreamdeckXTest):

    def test_init(self):
        """ButtonStyle.__init__"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(bs.name, 'My Style')
        self.assertEqual(bs.icon, 'icon.png')
        self.assertEqual(bs.font, 'Arial.ttf')
        self.assertEqual(bs.label, 'Press Me!')

    def test_str(self):
        """ButtonStyle.__str__"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(str(bs), 'My Style - Press Me! (icon.png, Arial.ttf)')

    def test_repr(self):
        """ButtonStyle.__repr__"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(repr(bs), 'My Style')

    def test_eq_equal(self):
        """ButtonStyle.__eq__.equal"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(bs1, bs2)

    def test_eq_diff_types(self):
        """ButtonStyle.__eq__.diff_types"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = True

        self.assertNotEqual(bs1, bs2)

    def test_eq_diff_names(self):
        """ButtonStyle.__eq__.diff_names"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = ButtonStyle('Your Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertNotEqual(bs1, bs2)

    def test_eq_diff_icons(self):
        """ButtonStyle.__eq__.diff_icons"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = ButtonStyle('My Style', 'up_arrow.png', 'Arial.ttf', 'Press Me!')

        self.assertNotEqual(bs1, bs2)

    def test_eq_diff_fonts(self):
        """ButtonStyle.__eq__.diff_fonts"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = ButtonStyle('Your Style', 'icon.png', 'Arial-Bold.ttf', 'Press Me!')

        self.assertNotEqual(bs1, bs2)

    def test_eq_diff_labels(self):
        """ButtonStyle.__eq__.diff_labels"""
        bs1 = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')
        bs2 = ButtonStyle('Your Style', 'icon.png', 'Arial.ttf', 'Don\'t Press Me!')

        self.assertNotEqual(bs1, bs2)

    def test_hash(self):
        """ButtonStyle.__hash__"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(hash(bs), hash('My Styleicon.pngArial.ttfPress Me!'))

    @patch('os.path.join')
    def test_icon_path(self, m_join):
        """ButtonStyle.icon_path"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        m_join.return_value = 'path/to/icon.png'
        icon_path = bs.icon_path

        m_join.assert_called_with(ButtonStyle.ASSETS_PATH, 'icon.png')
        self.assertEqual(icon_path, 'path/to/icon.png')

    @patch('os.path.join')
    def test_font_path(self, m_join):
        """ButtonStyle.font_path"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        m_join.return_value = 'path/to/Arial.ttf'
        font_path = bs.font_path

        m_join.assert_called_with(ButtonStyle.ASSETS_PATH, 'Arial.ttf')
        self.assertEqual(font_path, 'path/to/Arial.ttf')

    @patch('button_style.ButtonStyle._hex_to_rgb')
    def test_rgb_background_color(self, m_hex_to_rgb):
        bs = ButtonStyle('My Style', background_color='#010203')
        m_hex_to_rgb.return_value = (1, 2, 3)

        self.assertEqual((1, 2, 3), bs.rgb_background_color)

        m_hex_to_rgb.assert_called_with('#010203')

    @patch('button_style.ButtonStyle._hex_to_rgb')
    def test_rgb_text_color(self, m_hex_to_rgb):
        bs = ButtonStyle('My Style', text_color='#020406')
        m_hex_to_rgb.return_value = (2, 4, 6)

        self.assertEqual((2, 4, 6), bs.rgb_text_color)

        m_hex_to_rgb.assert_called_with('#020406')

    def test_hex_to_rgb_black(self):
        hex_color = '#000000'

        rgb = ButtonStyle._hex_to_rgb(hex_color)

        self.assertEqual((0, 0, 0), rgb)

    def test_hex_to_rgb_white(self):
        hex_color = '#ffffff'

        rgb = ButtonStyle._hex_to_rgb(hex_color)

        self.assertEqual((255, 255, 255), rgb)

    def test_hex_to_rgb_teal(self):
        hex_color = '#008080'

        rgb = ButtonStyle._hex_to_rgb(hex_color)

        self.assertEqual((0, 128, 128), rgb)

    def test_hex_to_rgb_red(self):
        hex_color = '#ee0000'

        rgb = ButtonStyle._hex_to_rgb(hex_color)

        self.assertEqual((238, 0, 0), rgb)


if __name__ == '__main__':
    unittest.main()
