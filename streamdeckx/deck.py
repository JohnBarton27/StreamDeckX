from StreamDeck.DeviceManager import DeviceManager


class Deck:

    def __init__(self):
        pass

    @staticmethod
    def get_connected():
        decks = DeviceManager().enumerate()

        for deck in decks:
            print(deck)