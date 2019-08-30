# Checkers pattern
import math
from Pattern import Pattern


class Checkers(Pattern):
    def __init__(self, a, b):
        super(Checkers, self).__init__()
        self.a = a
        self.b = b

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        if (math.floor(point.x) + math.floor(point.y) + math.floor(point.z)) \
         % 2 == 0:
            return self.a.pattern_at(point)
        else:
            return self.b.pattern_at(point)
