# Stripe pattern
import math
import Matrix


class Stripe(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.transform = Matrix.IdentityMatrix(4)

    def stripe_at(self, point):
        # Point is in the parent space (world, object, other pattern)
        # First transform to pattern space
        ppoint = self.inverse_transform * point
        if math.floor(ppoint.x) % 2 == 0:
            return self.a
        else:
            return self.b

    # Set the inverse transform every time we update the transform.
    # This should remove a lot of repeated calculations.
    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, val):
        self.__transform = val
        self.__inverse_transform = self.transform.inverse()
        self.__transpose_inverse_transform = \
            self.__inverse_transform.transpose()

    # Really want some way to block this from being set independently.
    # More reading to do.
    # Seems like just not providing a setter is good enough.
    @property
    def inverse_transform(self):
        return self.__inverse_transform

    @property
    def transpose_inverse_transform(self):
        return self.__transpose_inverse_transform
