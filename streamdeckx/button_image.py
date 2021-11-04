import io

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper


class ButtonImage:

    def __init__(self, style, deck):
        self.style = style
        self.deck = deck

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
        # (10, 52) is the (x-offset from left, y-offset from top)
        draw.text((10, 10), text=self.style.label, font=font, align="center", fill="white")

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

    def render_key_image(self):
        return PILHelper.to_native_format(self.deck.deck_interface, self.image)

    @staticmethod
    def get_text_dimensions(text_string, font):
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return text_width, text_height
