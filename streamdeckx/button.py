# from pillow import Image, ImageDraw, ImageFont
# from StreamDeck.DeviceManager import DeviceManager
# from StreamDeck.ImageHelpers import PILHelper


class Button:

    def __init__(self, position: int):
        """
        Constructor for Button class.

        Args:
            position (int): Position of this button on its Stream Deck. Positions start at 0 and are assigned
                left-to-right, top-to-bottom.
        """
        self.position = position
        self.actions = []

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
        html = f'<span id="{self.position}" class="btn" onclick="openConfig({self.position})"></span>'
        return html

    def add_action(self, action):
        """Add an action to this Button"""
        self.actions.append(action)

    def serialize(self):
        """Converts this button into its JSON representation, suitable for returning from an API"""
        return {
            "position": self.position
        }

    def display_text(self, text: str):
        """
        Displays the given text on this button.

        Returns:
            None
        """
        #img = Image.open('C:\Users\John\git\streamdeckx\streamdeckx\static\gradient_sq.png')
