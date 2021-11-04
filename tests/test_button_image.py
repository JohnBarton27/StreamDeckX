import unittest
from unittest.mock import patch, MagicMock

from button_image import ButtonImage


class TestButtonImage(unittest.TestCase):

    def setUp(self) -> None:
        get_text_dimensions_patch = patch('button_image.ButtonImage.get_text_dimensions')
        self.m_get_text_dimensions = get_text_dimensions_patch.start()
        self.addCleanup(get_text_dimensions_patch.stop)
        self.m_get_text_dimensions.side_effect = get_text_dimensions_side_effect

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


def get_text_dimensions_side_effect(line, font):
    # This just returns the 'length' (number of characters) of the string to make testing easier
    return len(line), 0


if __name__ == '__main__':
    unittest.main()
