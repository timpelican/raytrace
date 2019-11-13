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
        # However, we want the nested pattern to go from 0 to 1 within each
        # check, so we need to translate the point again before passing to
        # the inner function
        if (math.floor(point.x) + math.floor(point.y) + math.floor(point.z)) \
         % 2 == 0:
            return self.a.pattern_at(point.translate(-math.floor(point.x),
                                                     -math.floor(point.y),
                                                     -math.floor(point.z)))
        else:
            return self.b.pattern_at(point.translate(-math.floor(point.x),
                                                     -math.floor(point.y),
                                                     -math.floor(point.z)))
