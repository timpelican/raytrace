# Ring pattern
import math
from Pattern import Pattern


class RingPattern(Pattern):
    def __init__(self, a, b):
        super(RingPattern, self).__init__()
        self.a = a
        self.b = b

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        if math.floor(math.sqrt(point.x ** 2 + point.z ** 2)) % 2 == 0:
            return self.a.pattern_at(point)
        else:
            return self.b.pattern_at(point)
