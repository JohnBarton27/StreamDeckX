

class Button:

    def __init__(self, position: int):
        """
        Constructor for Button class.

        Args:
            position (int): Position of this button on its Stream Deck. Positions start at 0 and are assigned
                left-to-right, top-to-bottom.
        """
        self.position = position

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

    def serialize(self):
        """Converts this button into its JSON representation, suitable for returning from an API"""
        return {
            "position": self.position
        }


class EmptyButton(Button):
    """
    Class for a Button that has not been given any actions yet
    """


class TextButton(Button):
    """
    Class for a Button that, when pressed, types out a string of text.
    """

    def __init__(self, position: id, text: str):
        super().__init__(position)
        self.text = text

    def serialize(self):
        """Converts this button into its JSON representation, suitable for returning from an API"""
        json = super().serialize()
        json['text'] = self.text
        return json
