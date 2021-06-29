from StreamDeck.DeviceManager import DeviceManager


class Deck:
    generic_name = None
    cols = None
    rows = None

    def __init__(self, deck_id: str):
        self.id = deck_id

    @staticmethod
    def get_connected():
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            if deck.deck_type() == 'Stream Deck XL':
                deck_objs.append(XLDeck(deck.id))
            else:
                print(f'Unsupported deck type "{deck.deck_type()}"!')

        return deck_objs


class XLDeck(Deck):
    generic_name = 'Stream Deck XL'
    cols = 8
    rows = 4

    def __init__(self, deck_id: str):
        super().__init__(deck_id)
