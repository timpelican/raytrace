# Spheres
from Intersection import Intersection, Intersections
import Tuple4
import math


class Sphere(object):
    def __init__(self):
        pass

    def intersects(self, ray):
        # the vector from the sphere's center, to the ray origin
        # remember: the sphere is centered at the world origin
        sphere_to_ray = ray.origin - Tuple4.Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = math.pow(b, 2) - 4 * a * c
        if discriminant < 0:
            return ()
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self),
                             Intersection(t2, self))
