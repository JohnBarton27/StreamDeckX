import unittest

from button import Button, EmptyButton, TextButton


class TestButton(unittest.TestCase):
    def test_init(self):
        """Button.__init__"""
        button = Button(12)
        self.assertEqual(button.position, 12)

    def test_repr(self):
        """Button.__repr__"""
        button = Button(12)
        self.assertEqual(repr(button), '12')

    def test_str(self):
        """Button.__str__"""
        button = Button(12)
        self.assertEqual(str(button), '12')

    def test_eq_equal(self):
        """Button.__eq__.equal"""
        button1 = Button(12)
        button2 = Button(12)
        self.assertEqual(button1, button2)

    def test_eq_diff_positions(self):
        """Button.__eq__.diff_positions"""
        button1 = Button(12)
        button2 = Button(14)
        self.assertNotEqual(button1, button2)

    def test_hash(self):
        """Button.__hash__"""
        button = Button(12)
        self.assertEqual(hash(button), hash(12))

    def test_html(self):
        """Button.html"""
        button = Button(12)
        self.assertEqual(button.html, '<span id="12" class="btn"></span>')


class TestEmptyButton(unittest.TestCase):
    def test_init(self):
        """EmptyButton.__init__"""
        button = EmptyButton(1)
        self.assertEqual(button.position, 1)


class TestTextButton(unittest.TestCase):
    def test_init(self):
        """TextButton.__init__"""
        button = TextButton(2, 'username')
        self.assertEqual(button.position, 2)
        self.assertEqual(button.text, 'username')


if __name__ == '__main__':
    unittest.main()
