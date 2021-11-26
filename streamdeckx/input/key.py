import string


class Key:

    def __init__(self, val: str):
        self.val = val

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False

        return self.val == other.val

    def json(self):
        return {
            'value': self.val
        }

    @staticmethod
    def _get_for_vals(vals: list):
        key_list = []
        for val in vals:
            key_list.append(Key(val))

        return key_list

    @staticmethod
    def get_function_keys():
        return Key._get_for_vals([f'F{val}' for val in range(1, 21)])

    @staticmethod
    def get_alpha_keys():
        return Key._get_for_vals([char for char in string.ascii_lowercase])

    @staticmethod
    def get_num_keys():
        return Key._get_for_vals([str(num) for num in range(0,9)])

    @staticmethod
    def get_special_keys():
        special_keys = ['ALT', 'CTRL', 'DEL', 'ENTER', 'ESC', 'SHIFT']
        return Key._get_for_vals(special_keys)

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