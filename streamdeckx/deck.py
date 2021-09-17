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

    instantiated_decks = []

    def __init__(self, deck_id: str, name: str=None):
        if isinstance(deck_id, bytes):
            deck_id = deck_id.decode('utf-8')

        # The 'deck_id' provided by the Stream Deck API can have a lot of extra pieces -
        # this strips it down to what we actually need
        self.id = Deck._strip_id(deck_id)
        self.name = name
        self.buttons = []
        self._is_open = False

        if self.deck_interface:
            self.reset()

        # Populate with the correct number of (empty) buttons
        self.open()
        for i in range(0, self.__class__.get_num_buttons()):
            self.add_button(i)
        self.close()

        Deck.instantiated_decks.append(self)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name} ({self.id})'

    def add_button(self, index):
        self.buttons.append(Button(index, self))

    @functools.cached_property
    def deck_interface(self):
        decks = DeviceManager().enumerate()

        for deck in decks:
            if Deck._strip_id(deck.id()) == self.id:
                return deck

    def open(self):
        if not self._is_open and self.deck_interface:
            self.deck_interface.open()
            self._is_open = True

    def close(self):
        if self._is_open and self.deck_interface:
            self.deck_interface.close()
            self._is_open = False

    def reset(self):
        if not self.deck_interface:
            return

        self.open()
        self.deck_interface.reset()
        self.close()

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
    def _get_instantiated_deck_by_id(deck_id):
        for deck in Deck.instantiated_decks:
            if deck.id == deck_id:
                return deck

    @staticmethod
    def get_connected():
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            deck_id = Deck._strip_id(deck.id())

            # Check to see if we have already instantiated this deck
            instantiated_deck = Deck._get_instantiated_deck_by_id(deck.id())

            # If we haven't already instantiated it, we need to get it from the database
            if not instantiated_deck:
                instantiated_deck = Deck.deck_dao.get_by_id(deck_id)

            if instantiated_deck:
                deck_objs.append(instantiated_deck)
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
