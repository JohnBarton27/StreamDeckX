class ButtonStyle:

    def __init__(self, name: str, icon: str, font: str, label: str):
        self.name = name
        self.icon = icon
        self.font = font
        self.label = label

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
