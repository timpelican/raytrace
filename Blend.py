# Blend pattern
from Pattern import Pattern


class Blend(Pattern):
    def __init__(self, a, b):
        super(Blend, self).__init__()
        self.a = a
        self.b = b

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        # Return the simple average of colour returned by the two inner
        # patterns
        return (self.a.pattern_at(point) * 0.5) + \
               (self.b.pattern_at(point) * 0.5)
