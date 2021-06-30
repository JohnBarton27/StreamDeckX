

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
        html = f'<span id="{self.position}" class="btn"></div>'
        return html
