import base64
import io

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper


class ButtonImage:

    def __init__(self, style, deck):
        self.style = style
        self.deck = deck
        self._image_size = 0

    @property
    def image(self):
        background = Image.new('RGB', (100, 100), self.style.rgb_background_color)
        if self.style.background_image:
            background_image = Image.open(io.BytesIO(base64.b64decode(self.style.background_image))).convert('RGBA')
            background_image.load()
            background_image_scaled = background_image.resize((100, 100))
            background.paste(background_image_scaled, mask=background_image_scaled.split()[3])

        image = PILHelper.create_scaled_image(self.deck.deck_interface, background, margins=[0, 0, 0, 0])
        self._image_size = image.size[0]
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
        font = ImageFont.truetype(self.style.font_path, self.style.font_size)
        text_lines = self.get_split_text(font)
        max_width = ButtonImage.get_max_width(text_lines, font)

        outer_buffer = round((self._image_size - max_width) / 2)

        draw.text((outer_buffer, 10), text='\n'.join(text_lines), font=font, align="center", fill=self.style.rgb_text_color)

    def get_split_text(self, font):
        raw_text = self.style.label

        text_width = ButtonImage.get_text_dimensions(raw_text, font)[0]

        if text_width < self._image_size:
            return [raw_text]

        # Split by word
        split_text = raw_text.split(' ')
        text_lines = []
        curr_line = None

        for word in split_text:
            if not curr_line:
                curr_line = ImageLine([word], font)
                continue

            curr_line.stage_word(word)

            if curr_line.staged_width > self._image_size:
                # Went too far! Need to break off the last thing we added
                text_lines.append(str(curr_line))
                curr_line = ImageLine([word], font)
            else:
                # This word was "safe" to add, so add it
                curr_line.commit_staged_word()

        # Add the final (short enough) line
        text_lines.append(str(curr_line))
        return text_lines

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


class ImageLine:

    def __init__(self, words: list, font):
        self.words = words
        self.font = font
        self._staged_word = None

    def __repr__(self):
        return ' '.join(self.words)

    def __str__(self):
        return ' '.join(self.words)

    @property
    def width(self):
        return ButtonImage.get_text_dimensions(' '.join(self.words), self.font)[0]

    @property
    def staged_width(self):
        return ButtonImage.get_text_dimensions(' '.join(self.words + [self._staged_word]), self.font)[0]

    def stage_word(self, next_word):
        self._staged_word = next_word

    def commit_staged_word(self):
        self.words.append(self._staged_word)
        self._staged_word = None
