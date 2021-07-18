from abc import ABC
from PIL import Image, ImageDraw, ImageFont
import io
import functools
import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


class Deck(ABC):
    generic_name = None
    cols = None
    rows = None

    def __init__(self, deck_id: str):
        self.id = deck_id
        self.buttons = []
        self._generate_buttons()

        self.deck_interface.open()
        for key in range(self.deck_interface.key_count()):
            self.update_key_image(key, False)

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
        # Last button in the example application is the exit button.
        exit_key_index = self.deck_interface.key_count() - 1

        if key == exit_key_index:
            name = "exit"
            icon = "{}.png".format("Exit")
            font = "Roboto-Regular.ttf"
            label = "Bye" if state else "Exit"
        else:
            name = "emoji"
            icon = "{}.png".format("Pressed" if state else "Released")
            font = "Roboto-Regular.ttf"
            label = "Pressed!" if state else "Key {}".format(key)

        return {
            "name": name,
            "icon": os.path.join(ASSETS_PATH, icon),
            "font": os.path.join(ASSETS_PATH, font),
            "label": label
        }

    # Generates a custom tile with run-time generated text and custom image via the
    # PIL module.
    def render_key_image(self, icon_filename, font_filename, label_text):
        # Resize the source image asset to best-fit the dimensions of a single key,
        # leaving a margin at the bottom so that we can draw the key title
        # afterwards.
        icon = Image.open(icon_filename)
        image = PILHelper.create_scaled_image(self.deck_interface, icon, margins=[0, 0, 20, 0])

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_filename, 14)
        draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

        return PILHelper.to_native_format(self.deck_interface, image)

    def update_key_image(self, key, state):
        # Determine what icon and label to use on the generated key.
        key_style = self.get_key_style(key, state)

        # Generate the custom key with the requested image and label.
        image = self.render_key_image(key_style["icon"], key_style["font"], key_style["label"])

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
