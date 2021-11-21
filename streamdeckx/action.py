import logging
from abc import ABC, abstractmethod


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

    @abstractmethod
    def execute(self):
        pass


class ActionFactory:

    @staticmethod
    def get_by_type(action_type: str):
        if action_type == 'TEXT':
            return TextAction

        if action_type == 'MULTIKEY':
            return MultiKeyPressAction


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

    def execute(self):
        logging.info(f'Pressing: {"+".join(self.key_presses)}')

        from pynput.keyboard import Controller
        keyboard = Controller()

        for key_press in self.key_presses:
            keyboard.press(MultiKeyPressAction._get_key(key_press))

        for key_press in reversed(self.key_presses):
            keyboard.release(MultiKeyPressAction._get_key(key_press))

    @staticmethod
    def _get_key(text):
        from pynput.keyboard import Key

        if text == 'ALT':
            return Key.alt
        elif text == 'CTRL':
            return Key.ctrl
        elif text == 'F1':
            return Key.f1
        elif text == 'F2':
            return Key.f2
        elif text == 'F3':
            return Key.f3
        elif text == 'F4':
            return Key.f4
        elif text == 'F5':
            return Key.f5
        elif text == 'F6':
            return Key.f6
        elif text == 'F7':
            return Key.f7
        elif text == 'F8':
            return Key.f8
        elif text == 'F9':
            return Key.f9
        elif text == 'F10':
            return Key.f10
        elif text == 'F11':
            return Key.f11
        elif text == 'F12':
            return Key.f12
        elif text == 'F13':
            return Key.f13
        elif text == 'F14':
            return Key.f14
        elif text == 'F15':
            return Key.f15
        elif text == 'F16':
            return Key.f16
        elif text == 'F17':
            return Key.f17
        elif text == 'F18':
            return Key.f18
        elif text == 'F19':
            return Key.f19
        elif text == 'F20':
            return Key.f20
        elif text == 'OS':
            return Key.cmd
        elif text == 'SHIFT':
            return Key.shift
        elif text == 'TAB':
            return Key.tab
        else:
            return text


class ActionMissingIdError(Exception):
    """
    Raised when an Action needs an ID, but one has not been given/set.
    """
    pass
