import functools
import logging
import subprocess
import time
from abc import ABC, abstractmethod

from input.key import Key


class Action(ABC):

    def __init__(self, parameter: str, button, order: int, action_id: int = None):
        self.parameter = parameter
        self.button = button
        self.order = order
        self.id = action_id

    @property
    @abstractmethod
    def action_type(self):
        pass

    @property
    @abstractmethod
    def display_value(self):
        pass

    @abstractmethod
    def execute(self):
        pass


class TextAction(Action):
    """Class for an action that sends text"""

    @property
    def action_type(self):
        return 'TEXT'

    def __init__(self, parameter: str, button, order: int, action_id: int = None):
        super().__init__(parameter, button, order, action_id=action_id)
        self.text = parameter

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.text == other.text

    def __hash__(self):
        return hash(self.text)

    @property
    def display_value(self):
        return self.text

    def execute(self):
        logging.info(f'Printing: {self.text}')
        from pynput.keyboard import Controller

        keyboard = Controller()

        # Press and release space
        for char in self.text:
            keyboard.press(char)
            keyboard.release(char)


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


class DelayAction(Action):

    @property
    def action_type(self):
        return 'DELAY'

    def __init__(self, parameter: str, button, order: int, action_id: int = None):
        super().__init__(parameter, button, order, action_id=action_id)
        self.delay_time = int(parameter)

    @property
    def display_value(self):
        return f'{self.delay_time} seconds'

    def execute(self):
        time.sleep(self.delay_time)


class ApplicationAction(Action):

    @property
    def action_type(self):
        return 'APPLICATION'

    def __init__(self, parameter: str, button, order: int, action_id: int = None):
        super().__init__(parameter, button, order, action_id=action_id)
        self.application = parameter

    @property
    def display_value(self):
        return f'Open {self.application}'

    def execute(self):
        subprocess.call(self.application)


class ActionMissingIdError(Exception):
    """
    Raised when an Action needs an ID, but one has not been given/set.
    """
    pass
