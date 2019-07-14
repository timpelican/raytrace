# Spheres
from Intersection import Intersection, Intersections
import Tuple4
import math
import Matrix
import Material


class Sphere(object):
    def __init__(self):
        self.transform = Matrix.IdentityMatrix(4)
        self.material = Material.Material()

    def intersects(self, ray):
        # Transform the ray into object coordinate space
        ray2 = ray.transform(self.transform.inverse())
        # the vector from the sphere's center, to the ray origin
        # remember: the sphere is centered at the world origin
        sphere_to_ray = ray2.origin - Tuple4.Point(0, 0, 0)
        a = ray2.direction.dot(ray2.direction)
        b = 2 * ray2.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = math.pow(b, 2) - 4 * a * c
        if discriminant < 0:
            return Intersections()
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self),
                             Intersection(t2, self))

    def normal_at(self, world_p):
        object_p = self.inverse_transform * world_p
        object_n = object_p - Tuple4.Point(0, 0, 0)
        world_n = self.transpose_inverse_transform * object_n
        world_n.w = 0
        return world_n.normalize()

    def __str__(self):
        return 'Sphere(({t}), ({m}))'.format(t=self.transform,
                                             m=self.material)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.transform == other.transform and \
           self.material == other.material:
            return True
        else:
            return False

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
    @property
    def inverse_transform(self):
        return self.__inverse_transform

    # @inverse_transform.setter
    # def inverse_transform(self, val):
    #     self.__inverse_transform = val

    @property
    def transpose_inverse_transform(self):
        return self.__transpose_inverse_transform
