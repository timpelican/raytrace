# Stripe pattern
import Matrix
import Tuple4


class Pattern(object):
    def __init__(self):
        self.transform = Matrix.IdentityMatrix(4)

    def pattern_at(self, point):
        # Incoming point is in parent space, apply our inverse transform
        ppoint = self.inverse_transform * point
        return self.pattern(ppoint)

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


class TestPattern(Pattern):
    def pattern(self, point):
        return Tuple4.Colour(point.x, point.y, point.z)
