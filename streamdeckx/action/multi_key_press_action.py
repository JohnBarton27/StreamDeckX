import functools
import logging

from action.action import Action
from input.key import Key


class MultiKeyPressAction(Action):
    """Class for an action where multiple keys are pressed at once"""

    all_keys = Key.get_all_keys()

    @property
    def action_type(self):
        return 'MULTIKEY'

    def __init__(self, parameter: str, button, order: int, action_id: int = None):
        super().__init__(parameter, button, order, action_id=action_id)
        self.key_presses = parameter.split(';')

    def __repr__(self):
        return '+'.join(self.key_presses)

    def __str__(self):
        return '+'.join(self.key_presses)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        if len(self.key_presses) != len(other.key_presses):
            return False

        # Ensure all key presses in our list exist in the other
        return all([key in other.key_presses for key in self.key_presses])

    def __hash__(self):
        return hash('+'.join(self.key_presses))

    @functools.cached_property
    def keys(self):
        keys = []
        for key_press in self.key_presses:
            keys.append(MultiKeyPressAction._get_key(key_press))

        return keys

    @property
    def display_value(self):
        return ' + '.join(self.key_presses)

    def execute(self):
        logging.info(f'Pressing: {"+".join(self.key_presses)}')

        for key in self.keys:
            key.press()

        for key in reversed(self.keys):
            key.release()

    @staticmethod
    def _get_key(text):
        for key in MultiKeyPressAction.all_keys:
            if key.name == text:
                return key
