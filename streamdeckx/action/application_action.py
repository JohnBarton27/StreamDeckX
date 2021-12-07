import subprocess

from action.action import Action


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
