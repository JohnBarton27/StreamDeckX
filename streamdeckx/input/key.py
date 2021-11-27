import string

try:
    from pynput.keyboard import Key as pkey
    from pynput.keyboard import Controller
except ImportError:
    from unittest.mock import MagicMock
    pkey = MagicMock()  # Unit testing
    Controller = MagicMock()


class Key:

    controller = Controller()

    def __init__(self, name: str, pykey: pkey):
        self.name = name
        self.pkey = pykey

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False

        return self.name == other.name

    def json(self):
        return {
            'value': self.name
        }

    def press(self):
        Key.controller.press(self.pkey)

    def release(self):
        Key.controller.release(self.pkey)

    @staticmethod
    def get_function_keys():
        return [Key('F1', pkey.f1),
                Key('F2', pkey.f2),
                Key('F3', pkey.f3),
                Key('F4', pkey.f4),
                Key('F5', pkey.f5),
                Key('F6', pkey.f6),
                Key('F7', pkey.f7),
                Key('F8', pkey.f8),
                Key('F9', pkey.f9),
                Key('F10', pkey.f10),
                Key('F11', pkey.f11),
                Key('F12', pkey.f12),
                Key('F13', pkey.f13),
                Key('F14', pkey.f14),
                Key('F15', pkey.f15),
                Key('F16', pkey.f16),
                Key('F17', pkey.f17),
                Key('F18', pkey.f18),
                Key('F19', pkey.f19),
                Key('F20', pkey.f20),
                Key('F21', pkey.f21),
                Key('F22', pkey.f22),
                Key('F23', pkey.f23),
                Key('F24', pkey.f24)]

    @staticmethod
    def get_alpha_keys():
        return [Key(char, char) for char in string.ascii_lowercase]

    @staticmethod
    def get_num_keys():
        return [Key(str(num), str(num)) for num in range(0, 10)]

    @staticmethod
    def get_special_keys():
        return [Key('ALT', pkey.alt),
                Key('BACKSPACE', pkey.backspace),
                Key('CAPS LOCK', pkey.caps_lock),
                Key('CMD', pkey.cmd),
                Key('CTRL', pkey.ctrl),
                Key('DELETE', pkey.delete),
                Key('DOWN ARROW', pkey.down),
                Key('END', pkey.end),
                Key('ENTER', pkey.enter),
                Key('ESC', pkey.esc),
                Key('HOME', pkey.home),
                Key('LEFT ARROW', pkey.left),
                Key('PAGE DOWN', pkey.page_down),
                Key('PAGE UP', pkey.page_up),
                Key('RIGHT ARROW', pkey.right),
                Key('SHIFT', pkey.shift),
                Key('SPACE', pkey.space),
                Key('TAB', pkey.tab),
                Key('UP ARROW', pkey.up),
                Key('INSERT', pkey.insert),
                Key('MENU', pkey.menu),
                Key('NUM LOCK', pkey.num_lock),
                Key('PRINT SCREEN', pkey.print_screen),
                Key('SCROLL LOCK', pkey.scroll_lock)]

    @staticmethod
    def get_all_keys():
        return Key.get_function_keys() + Key.get_alpha_keys() + Key.get_num_keys() + Key.get_special_keys()


class KeyGroup:

    def __init__(self, name: str, keys: list):
        self.name = name
        self.keys = keys

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def json(self):
        return {
            'keys': [key.json() for key in self.keys],
            'name': self.name
        }

    @staticmethod
    def get_all():
        special_keys = KeyGroup('Special', Key.get_special_keys())
        alpha_keys = KeyGroup('Alpha', Key.get_alpha_keys())
        num_keys = KeyGroup('Numbers', Key.get_num_keys())
        function_keys = KeyGroup('Function', Key.get_function_keys())

        return [special_keys, alpha_keys, num_keys, function_keys]
