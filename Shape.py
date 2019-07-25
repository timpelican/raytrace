# Abstract behaviours common to all shapes
import Matrix
import Material
import Tuple4


class Shape(object):
    def __init__(self):
        self.transform = Matrix.IdentityMatrix(4)
        self.material = Material.Material()

    def intersects(self, ray):
        # Transform the ray into object coordinate space
        ray2 = ray.transform(self.inverse_transform)
        # Intersect the transformed ray with the concrete implementation
        # of an intersection
        return self.local_intersects(ray2)

    def normal_at(self, point):
        # Transform the point to object space
        local_point = self.inverse_transform * point
        # Find the concrete normal in object space
        local_normal = self.local_normal_at(local_point)
        # Transform back to world space
        world_normal = self.transpose_inverse_transform * local_normal
        world_normal.w = 0
        return world_normal.normalize()

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


class TestShape(Shape):
    def local_intersects(self, ray):
        # We don't care about the actual intersect for the
        # test class, just save the transformed ray so we can
        # later confirm it has been transformed.
        self.saved_ray = ray
        return []

    def local_normal_at(self, point):
        # For test purposes, return the point as a vector
        return Tuple4.Vector(point.x, point.y, point.z)
