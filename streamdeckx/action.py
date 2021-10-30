from abc import ABC, abstractmethod
import logging


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


class ActionMissingIdError(Exception):
    """
    Raised when an Action needs an ID, but one has not been given/set.
    """
    pass
