import unittest

from button_style import ButtonStyle


class TestButtonStyle(unittest.TestCase):

    def test_init(self):
        """ButtonStyle.__init__"""
        bs = ButtonStyle('My Style', 'icon.png', 'Arial.ttf', 'Press Me!')

        self.assertEqual(bs.name, 'My Style')
        self.assertEqual(bs.icon, 'icon.png')
        self.assertEqual(bs.font, 'Arial.ttf')
        self.assertEqual(bs.label, 'Press Me!')


if __name__ == '__main__':
    unittest.main()
