import time

from action.action import Action


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
