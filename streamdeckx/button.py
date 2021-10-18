import io

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper

from button_style import ButtonStyle
from dao.button_dao import ButtonDao


class Button:

    button_dao = ButtonDao()

    def __init__(self, position: int, deck, btn_id: int = None, style: ButtonStyle = None):
        """
        Constructor for Button class.

        Args:
            position (int): Position of this button on its Stream Deck. Positions start at 0 and are assigned
                left-to-right, top-to-bottom.
            deck (Deck): Deck object that this Button belongs to
            btn_id (int): Database ID of the button (default: None)
            style (ButtonStyle): Style of the Button (text/image/font/etc.)
        """
        self.position = position
        self.deck = deck
        self.id = btn_id
        self.actions = []
        self.style = style if style else ButtonStyle('text', font='Roboto-Regular.ttf', label=f'{self.position}')

    def __repr__(self):
        return str(self.position)

    def __str__(self):
        return str(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    @property
    def html(self):
        """
        Generates the HTML for displaying this button on the page

        Returns:
            str: HTML representing this button
        """
        html = f'<span id="{self.position}" class="btn" onclick="openConfig({self.position})">' \
               f'<img id="{self.position}-img" height="72" width="72" src="data:image/PNG;base64, {self.image_bytes.decode("utf-8")}">' \
               f'</span>'
        return html

    @property
    def image(self):
        # Resize the source image asset to best-fit the dimensions of a single key,
        # leaving a margin at the bottom so that we can draw the key title
        # afterwards.
        icon = Image.open(self.style.icon_path)

        image = PILHelper.create_scaled_image(self.deck.deck_interface, icon, margins=[0, 0, 0, 0])

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(self.style.font_path, 16)
        draw.text((10, 52), text=self.style.label, font=font, align="center", fill="white")

        return image

    @property
    def image_bytes(self):
        """
        Returns the image in its 64-bit encoded bytes format.

        Returns:
            bytes: Image
        """
        import base64
        image = self.image

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return base64.b64encode(img_byte_arr.getvalue())

    def set_text(self, text: str):
        """
        Sets the text of this Button.

        Args:
            text (str): Text to apply to this Button
        """
        self.style.label = text
        self.deck.open()
        self.update_key_image()
        self.deck.close()

        # Update in database
        Button.button_dao.update(self)

    def add_action(self, action):
        """Add an action to this Button"""
        self.actions.append(action)

    def serialize(self):
        """Converts this button into its JSON representation, suitable for returning from an API"""
        return {
            "style": self.style.serialize(),
            "position": self.position
        }

    # Generates a custom tile with run-time generated text and custom image via the
    # PIL module.
    def render_key_image(self):
        return PILHelper.to_native_format(self.deck.deck_interface, self.image)

    def update_key_image(self):
        # Generate the custom key with the requested image and label.
        image = self.render_key_image()

        # Update requested key with the generated image.
        self.deck.open()
        self.deck.deck_interface.set_key_image(self.position, image)
        self.deck.close()
