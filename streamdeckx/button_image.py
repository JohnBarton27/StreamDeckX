import io

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper


class ButtonImage:

    def __init__(self, style, deck):
        self.style = style
        self.deck = deck
        self.image_size = 0

    @property
    def image(self):
        icon = Image.open(self.style.icon_path)

        image = PILHelper.create_scaled_image(self.deck.deck_interface, icon, margins=[0, 0, 0, 0])
        self.image_size = image.size[0]
        self.draw_text(ImageDraw.Draw(image))

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

    def draw_text(self, draw):
        font = ImageFont.truetype(self.style.font_path, 16)
        text_lines = self.get_split_text(font)
        max_width = ButtonImage.get_max_width(text_lines, font)

        outer_buffer = round((self.image_size - max_width) / 2)

        draw.text((outer_buffer, 10), text='\n'.join(text_lines), font=font, align="center", fill="white")

    def get_split_text(self, font):
        raw_text = self.style.label

        text_width = ButtonImage.get_text_dimensions(raw_text, font)[0]

        if text_width > self.image_size:
            # Split by word
            split_text = raw_text.split(' ')
            text_lines = []

            curr_line = []
            for word in split_text:
                curr_line.append(word)
                line_width = ButtonImage.get_text_dimensions(' '.join(curr_line), font)[0]

                if line_width > self.image_size:
                    # Went too far! Need to break off the last thing we added
                    words_for_line = curr_line[:-1]
                    text_lines.append(' '.join(words_for_line))

                    curr_line = [curr_line[-1]]

            # Add the final (short enough) line
            text_lines.append(' '.join(curr_line))
            return text_lines

        return [raw_text]

    @staticmethod
    def get_max_width(text_lines, font):
        max_width = 0

        for line in text_lines:
            line_width = ButtonImage.get_text_dimensions(line, font)[0]
            max_width = max(max_width, line_width)

        return max_width

    @staticmethod
    def get_text_dimensions(text_string, font):
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return text_width, text_height
