# Spheres
from Intersection import Intersection, Intersections
from Shape import Shape
import Tuple4
import math


class Sphere(Shape):
    def __init__(self):
        super(Sphere, self).__init__()

    def local_intersects(self, ray):
        # Incoming ray is now in object space already
        # the vector from the sphere's center, to the ray origin
        # remember: the sphere is centered at the world origin
        sphere_to_ray = ray.origin - Tuple4.Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = math.pow(b, 2) - 4 * a * c
        if discriminant < 0:
            return Intersections()
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        # Intersections are a scalar and an object, so we don't need to
        # transform them back to world space
        return Intersections(Intersection(t1, self),
                             Intersection(t2, self))

    def local_normal_at(self, object_p):
        # This works entirely in object space
        object_n = object_p - Tuple4.Point(0, 0, 0)
        return object_n

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
