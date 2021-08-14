import unittest
from unittest.mock import patch

from button_style import ButtonStyle


class TestButtonStyle(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
