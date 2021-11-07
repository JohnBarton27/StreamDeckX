import functools
import os


class ButtonStyle:

    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

    def __init__(self, name: str, icon: str = 'blank.png', font: str = 'Roboto-Regular.ttf', label: str = '', background_color: str ='#000000', text_color: str = '#ffffff'):
        self.name = name
        self.icon = icon
        self.font = font
        self.label = label
        self.background_color = background_color
        self.text_color = text_color

    def __str__(self):
        return f'{self.name} - {self.label} ({self.icon}, {self.font})'

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        # Type checking
        if not isinstance(other, ButtonStyle):
            return False

        # Name
        if not self.name == other.name:
            return False

        # Icon
        if not self.icon == other.icon:
            return False

        # Font
        if not self.font == other.font:
            return False

        # Label
        return self.label == other.label

    def __hash__(self):
        return hash(f'{self.name}{self.icon}{self.font}{self.label}')

    @functools.cached_property
    def icon_path(self):
        if not self.icon:
            return None

        return os.path.join(ButtonStyle.ASSETS_PATH, self.icon)

    @functools.cached_property
    def font_path(self):
        if not self.font:
            return None

        return os.path.join(ButtonStyle.ASSETS_PATH, self.font)

    def serialize(self):
        return {
            'label': self.label
        }
