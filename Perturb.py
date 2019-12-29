# Perturbation pattern
from Pattern import Pattern
from Tuple4 import Point
import Noise


class Perturb(Pattern):
    def __init__(self, a):
        super(Perturb, self).__init__()
        self.a = a
        # How do we accept or generate a seed?
        # Needs to be consistent for a given object, or animations will
        # fail badly.
        self.noise = Noise.Noise()
        # How much to scale the perturbation
        self.size = 0.1

    def pattern(self, point):
        # Incoming point has already been transformed into pattern space
        # by the parent Pattern class
        # Shift x, y and z by an amount of noise before passing to the
        # inner pattern.
        x = point.x
        y = point.y
        z = point.z
        dx = self.noise.eval2d(y, z) * self.size
        dy = self.noise.eval2d(x, z) * self.size
        dz = self.noise.eval2d(x, y) * self.size
        pp = Point(x + dx, y + dy, z + dz)
        # Return the simple average of colour returned by the two inner
        # patterns
        return self.a.pattern_at(pp)
