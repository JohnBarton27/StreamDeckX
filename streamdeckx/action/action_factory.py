from action.action import MultiKeyPressAction, DelayAction
from action.text_action import TextAction


class ActionFactory:

    @staticmethod
    def get_by_type(action_type: str):
        if action_type == 'TEXT':
            return TextAction

        if action_type == 'MULTIKEY':
            return MultiKeyPressAction

        if action_type == 'DELAY':
            return DelayAction
