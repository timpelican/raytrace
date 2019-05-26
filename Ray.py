# Rays are cast into the scene
# They have an origin and a direction


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + self.direction * t

    def transform(self, transform):
        return Ray(transform * self.origin, transform * self.direction)

    def __str__(self):
        return '(({o}), ({d}))'.format(o=self.origin, d=self.direction)
