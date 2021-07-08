from abc import ABC


class Action(ABC):
    pass


class TextAction(Action):
    """Class for an action that sends text"""

    def __init__(self, text: str):
        self.text = text

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
