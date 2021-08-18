from abc import ABC
import functools
import logging
import re
import os

from StreamDeck.DeviceManager import DeviceManager

from button import Button
from button_style import ButtonStyle
from dao.deck_dao import DeckDao
from deck_types import DeckTypes

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class Deck(ABC):
    generic_name = None
    cols = None
    rows = None

    deck_dao = DeckDao()

    def __init__(self, deck_id: str, name: str=None):
        if isinstance(deck_id, bytes):
            deck_id = deck_id.decode('utf-8')

        # The 'deck_id' provided by the Stream Deck API can have a lot of extra pieces -
        # this strips it down to what we actually need
        self.id = Deck._strip_id(deck_id)
        self.name = name
        self.buttons = []

        # Populate with the correct number of (empty) buttons
        for i in range(0, self.__class__.get_num_buttons()):
            self.buttons.append(Button(i, self))

        if self.deck_interface:
            self.deck_interface.open()
            self.deck_interface.reset()

    @functools.cached_property
    def deck_interface(self):
        decks = DeviceManager().enumerate()

        for deck in decks:
            if deck.id() == self.id:
                return deck

    @classmethod
    def get_num_buttons(cls):
        return cls.cols * cls.rows

    @staticmethod
    def _strip_id(full_id):
        if full_id.startswith('\\'):
            p = re.compile('{(.*)}')
            result = p.search(full_id)
            return result.group(1)
        else:
            return full_id

    @staticmethod
    def get_connected():
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            deck_id = Deck._strip_id(deck.id())
            deck_from_db = Deck.deck_dao.get_by_id(deck_id)
            logging.info(f'Deck from DB: {deck_from_db}')

            if deck_from_db:
                deck_objs.append(deck_from_db)
                continue

            if deck.deck_type() == DeckTypes.XL.value:
                deck_obj = XLDeck(deck.id())
                Deck.deck_dao.create(deck_obj)
                deck_objs.append(deck_obj)
            elif deck.deck_type() == DeckTypes.ORIGINAL.value:
                deck_obj = OriginalDeck(deck.id())
                Deck.deck_dao.create(deck_obj)
                deck_objs.append(deck_obj)
            else:
                print(f'Unsupported deck type "{deck.deck_type()}"!')

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
    type = DeckTypes.XL
    cols = 8
    rows = 4

    def __init__(self, deck_id: str):
        super().__init__(deck_id, name=str(self.__class__.type.value))


class OriginalDeck(Deck):
    type = DeckTypes.ORIGINAL
    cols = 5
    rows = 3

    def __init__(self, deck_id: str):
        super().__init__(deck_id, name=str(self.__class__.type.value))


class MiniDeck(Deck):
    type = DeckTypes.MINI
    cols = 3
    rows = 2

    def __init__(self, deck_id: str):
        super().__init__(deck_id, name=str(self.__class__.type.value))
