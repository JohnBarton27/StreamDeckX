import subprocess
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

    @property
    @abstractmethod
    def display_value(self):
        pass

    @abstractmethod
    def execute(self):
        pass


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
