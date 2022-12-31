from button_image import ButtonImage
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
        self.button_image = ButtonImage(self.style, self.deck)

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
               f'<img id="{self.position}-img" height="72" width="72" src="data:image/PNG;base64, {self.button_image.image_bytes.decode("utf-8")}">' \
               f'</span>'
        return html

    def set_text(self, text: str):
        """
        Sets the text of this Button.

        Args:
            text (str): Text to apply to this Button
        """
        self.style.label = text

        if self.deck.__class__.__name__ != 'VirtualDeck':
            self.update_key_image()

        # Update in database
        Button.button_dao.update(self)

    def set_colors(self, text_color: str, background_color: str):
        """
        Sets the colors of this button. Expects colors to be in the format 'f######'.

        Args:
            text_color (str): The color of any text in the button
            background_color (str): The color of the button's background
        """
        self.style.text_color = text_color
        self.style.background_color = background_color
        self.update_key_image()

        Button.button_dao.update(self)

    def set_font_size(self, font_size: int):
        """
        Sets the font size used on this button. Expects an integer.

        Args:
            font_size (int): Size of the font to be used on this button
        """
        self.style.font_size = font_size
        self.update_key_image()

        Button.button_dao.update(self)

    def set_background_image(self, background_image: str):
        self.style.background_image = background_image
        self.update_key_image()

        Button.button_dao.update(self)

    def add_action(self, action):
        """Add an action to this Button"""
        self.actions.append(action)

    def execute_actions(self):
        if not self.actions:
            return
        
        for action in self.actions:
            action.execute()

    def serialize(self):
        """Converts this button into its JSON representation, suitable for returning from an API"""
        return {
            "style": self.style.serialize(),
            "position": self.position
        }

    def update_key_image(self):
        # Generate the custom key with the requested image and label.
        image = self.button_image.render_key_image()

        # Update requested key with the generated image.
        if self.deck.__class__.__name__ != 'VirtualDeck':
            self.deck.deck_interface.set_key_image(self.position, image)


class ButtonMissingIdError(Exception):
    """
    Raised when a Button needs an ID, but one has not been given/set.
    """
    pass
