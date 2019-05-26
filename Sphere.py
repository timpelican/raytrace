# Spheres
from Intersection import Intersection, Intersections
import Tuple4
import math
import Matrix


class Sphere(object):
    def __init__(self):
        self.transform = Matrix.IdentityMatrix(4)

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
            return ()
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self),
                             Intersection(t2, self))
