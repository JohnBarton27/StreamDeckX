from abc import ABC
import functools
import re
import os

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

from button_style import ButtonStyle

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class Deck(ABC):
    generic_name = None
    cols = None
    rows = None

    def __init__(self, deck_id: str):
        # The 'deck_id' provided by the Stream Deck API can have a lot of extra pieces -
        # this strips it down to what we actually need
        if deck_id.startswith('\\'):
            p = re.compile('{(.*)}')
            result = p.search(deck_id)
            self.id = result.group(1)
        else:
            self.id = deck_id
        self.buttons = []
        self._generate_buttons()

        # self.deck_interface.open()
        # self.deck_interface.reset()
        # self.update_key_image(0, False)

    @functools.cached_property
    def deck_interface(self):
        decks = DeviceManager().enumerate()

        for deck in decks:
            if deck.id() == self.id:
                return deck

    def _generate_buttons(self):
        from button import Button
        for i in range(0, self.__class__.cols * self.__class__.rows):
            self.buttons.append(Button(i))

    # Returns styling information for a key based on its position and state.
    def get_key_style(self, key, state):

        style = ButtonStyle('emoji',
                            '{}.png'.format('Pressed' if state else 'Released'),
                            'Roboto-Regular.ttf',
                            'Pressed!' if state else 'Key {}'.format(key))

        return style

    # Generates a custom tile with run-time generated text and custom image via the
    # PIL module.
    def render_key_image(self, key_style):
        # Resize the source image asset to best-fit the dimensions of a single key,
        # leaving a margin at the bottom so that we can draw the key title
        # afterwards.
        icon = Image.open(key_style.icon_path)
        image = PILHelper.create_scaled_image(self.deck_interface, icon, margins=[0, 0, 20, 0])

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(key_style.font_path, 14)
        draw.text((image.width / 2, image.height - 5), text=key_style.label, font=font, anchor="ms", fill="white")

        return PILHelper.to_native_format(self.deck_interface, image)

    def update_key_image(self, key, state):
        # Determine what icon and label to use on the generated key.
        key_style = self.get_key_style(key, state)

        # Generate the custom key with the requested image and label.
        image = self.render_key_image(key_style)

        # Use a scoped-with on the deck to ensure we're the only thread using it
        # right now.
        with self.deck_interface:
            # Update requested key with the generated image.
            self.deck_interface.set_key_image(key, image)

    @staticmethod
    def get_connected():
        decks = DeviceManager().enumerate()
        deck_objs = []

        for deck in decks:
            if deck.deck_type() == 'Stream Deck XL':
                deck_objs.append(XLDeck(deck.id()))
            elif deck.deck_type() == 'Stream Deck Original':
                deck_objs.append(OriginalDeck(deck.id()))
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
