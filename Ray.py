# Rays are cast into the scene
# They have an origin and a direction


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + self.direction * t
