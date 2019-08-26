# Solid colour "pattern"
from Pattern import Pattern


class SolidColour(Pattern):
    def __init__(self, c):
        super(SolidColour, self).__init__()
        self.c = c

    def pattern(self, point):
        # Solid colour, this is in preparation for nesting patterns
        return self.c
