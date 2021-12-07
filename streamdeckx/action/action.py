import subprocess
import time
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
