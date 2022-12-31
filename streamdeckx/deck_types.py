from enum import Enum


class DeckTypes(Enum):

    XL = 'Stream Deck XL'
    ORIGINAL = 'Stream Deck Original'
    MINI = 'Stream Deck Mini'
    VIRTUAL = 'Virtual Stream Deck'

    @staticmethod
    def get_by_name(name):
        for deck_type in DeckTypes:
            if deck_type.name == name:
                return deck_type
