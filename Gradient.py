# Gradient pattern
import math
from Pattern import Pattern


class Gradient(Pattern):
    def __init__(self, a, b):
        super(Gradient, self).__init__()
        self.a = a
        self.b = b

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        # Gradient only makes sense with SolidColour children
        # TODO: should we enforce this at init?  Check for it here?
        distance = self.b.c - self.a.c
        fraction = point.x - math.floor(point.x)
        return self.a.c + distance * fraction


class BiGradient(Pattern):
    def __init__(self, a, b):
        super(BiGradient, self).__init__()
        self.a = a
        self.b = b

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        # BiGradient only makes sense with SolidColour children
        # TODO: should we enforce this at init?  Check for it here?
        # BiGradient goes from colour A to colour B and back again in one
        # unit, so there are no sharp transitions at each stripe
        distance = self.b.c - self.a.c
        fraction = point.x - math.floor(point.x)
        if fraction < 0.5:
            return self.a.c + distance * fraction * 2
        else:
            return self.b.c - distance * (fraction - 0.5) * 2
