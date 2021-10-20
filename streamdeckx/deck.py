import functools
import os
import re
from abc import ABC

from StreamDeck.DeviceManager import DeviceManager

from button import Button
from dao.action_dao import ActionDao
from dao.deck_dao import DeckDao
from deck_types import DeckTypes

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class Deck(ABC):
    generic_name = None
    cols = None
    rows = None

    deck_dao = DeckDao()

    instantiated_decks = []
    mappings = []

    def __init__(self, deck_id: str, name: str = None, buttons: list = None, session_id: str = None):
        # The 'deck_id' is actually the Stream Deck's Serial Number
        self.id = deck_id
        self.name = name
        self.buttons = buttons if buttons else []
        self._is_open = False
        self.session_id = session_id

        if not self.buttons:
            # Populate with the correct number of (empty) buttons
            for i in range(0, self.__class__.get_num_buttons()):
                self.add_button(i)

        Deck.instantiated_decks.append(self)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name} ({self.id})'

    def add_button(self, index):
        self.buttons.append(Button(index, self))

    @staticmethod
    def key_change_callback(deck, key, state):
        if not state:
            # Button was released
            return

        # Print new key state
        print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

        deck = Deck._get_instantiated_deck_by_id(deck.id())
        button = deck.buttons[key]

        action_dao = ActionDao()
        actions = action_dao.get_for_button(button)

        for action in actions:
            action.execute()

    def set_callbacks(self):
        self.deck_interface.set_key_callback(Deck.key_change_callback)

    @functools.cached_property
    def deck_interface(self):
        decks = DeviceManager().enumerate()

        for deck in decks:
            serial_num = Deck._get_serial_from_session_id(deck.id())

            if serial_num == self.id:
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

        self.deck_interface.reset()

    def update(self):
        for button in self.buttons:
            button.update_key_image()

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
            if deck.session_id == deck_id:
                return deck

    @staticmethod
    def _get_serial_from_session_id(session_id: str):
        for mapping in Deck.mappings:
            if mapping['session_id'] == session_id:
                return mapping['serial_number']

    @staticmethod
    def get_connected(update_images: bool = False):
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            deck_id = deck.id()

            if not any(deck_id == mapping['session_id'] for mapping in Deck.mappings):
                # If this is a new/unrecognized session, get its serial number
                deck.open()
                serial_num = deck.get_serial_number()
                deck.close()
            else:
                # We must already have the serial number
                serial_num = Deck._get_serial_from_session_id(deck_id)

            Deck.mappings.append({'session_id': deck_id, 'serial_number': serial_num})

            # Check to see if we have already instantiated this deck
            instantiated_deck = Deck._get_instantiated_deck_by_id(deck_id)

            # If we haven't already instantiated it, we need to get it from the database
            if not instantiated_deck:
                instantiated_deck = Deck.deck_dao.get_by_id(serial_num)

            if instantiated_deck:
                instantiated_deck.session_id = deck_id
                deck_objs.append(instantiated_deck)
                if update_images:
                    instantiated_deck.update()
                continue

            if deck.deck_type() == DeckTypes.XL.value:
                deck_obj = XLDeck(serial_num, session_id=deck_id)
                Deck.deck_dao.create(deck_obj)
                deck_objs.append(deck_obj)
                if update_images:
                    deck_obj.update()
            elif deck.deck_type() == DeckTypes.ORIGINAL.value:
                deck_obj = OriginalDeck(serial_num, session_id=deck_id)
                Deck.deck_dao.create(deck_obj)
                deck_objs.append(deck_obj)
                if update_images:
                    deck_obj.update()
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

    def __init__(self, deck_id: str, buttons: list = None, session_id: str = None):
        super().__init__(deck_id, name=str(self.__class__.type.value), buttons=buttons, session_id=session_id)


class OriginalDeck(Deck):
    type = DeckTypes.ORIGINAL
    cols = 5
    rows = 3

    def __init__(self, deck_id: str, buttons: list = None, session_id: str = None):
        super().__init__(deck_id, name=str(self.__class__.type.value), buttons=buttons, session_id=session_id)


class MiniDeck(Deck):
    type = DeckTypes.MINI
    cols = 3
    rows = 2

    def __init__(self, deck_id: str, buttons: list = None, session_id: str = None):
        super().__init__(deck_id, name=str(self.__class__.type.value), buttons=buttons, session_id=session_id)
