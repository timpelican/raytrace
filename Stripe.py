# Stripe pattern
import math


class Stripe(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def stripe_at(self, point):
        if math.floor(point.x) % 2 == 0:
            return self.a
        else:
            return self.b
