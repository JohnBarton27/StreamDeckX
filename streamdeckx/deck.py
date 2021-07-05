from abc import ABC
from StreamDeck.DeviceManager import DeviceManager


class Deck(ABC):
    generic_name = None
    cols = None
    rows = None

    def __init__(self, deck_id: str):
        self.id = deck_id
        self.buttons = []
        self._generate_buttons()

    def _generate_buttons(self):
        from button import Button
        for i in range(0, self.__class__.cols * self.__class__.rows):
            self.buttons.append(Button(i))

    @staticmethod
    def get_connected(add_testing=False):
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            if deck.deck_type() == 'Stream Deck XL':
                deck_objs.append(XLDeck(deck.id()))
            elif deck.deck_type() == 'Stream Deck Original':
                deck_objs.append(OriginalDeck(deck.id()))
            else:
                print(f'Unsupported deck type "{deck.deck_type()}"!')

        if add_testing:
            deck_objs.append(OriginalDeck('abc123'))
            deck_objs.append(MiniDeck('def456'))

        return deck_objs

    @property
    def html(self):
        html = ''
        position = 0
        for row in range(0, self.__class__.rows):
            html += '<br/>'
            for column in range(0, self.__class__.cols):
                html += self.buttons[position].html
                position += 1

        return html


class XLDeck(Deck):
    generic_name = 'Stream Deck XL'
    cols = 8
    rows = 4

    def __init__(self, deck_id: str):
        super().__init__(deck_id)


class OriginalDeck(Deck):
    generic_name = 'Stream Deck (Original)'
    cols = 5
    rows = 3


class MiniDeck(Deck):
    generic_name = 'Stream Deck Mini'
    cols = 3
    rows = 2
