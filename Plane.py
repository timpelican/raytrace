# Planes
from Intersection import Intersection, Intersections
from Shape import Shape
import Tuple4
import maths


class Plane(Shape):
    def __init__(self):
        super(Plane, self).__init__()

    def local_intersects(self, ray):
        # Incoming ray is now in object space already
        # If the ray is parallel to the plane (y = 0), there
        # is no intersection
        if maths.equals(ray.direction.y, 0):
            return Intersections()
        else:
            # Otherwise, the ray is intersecting from above
            # or below
            t = -ray.origin.y / ray.direction.y
            return Intersections(Intersection(t, self))

    def local_normal_at(self, object_p):
        # This works entirely in object space
        # The normal for a plane is fixed
        object_n = Tuple4.Vector(0, 1, 0)
        return object_n

    def __str__(self):
        return 'Plane(({t}), ({m}))'.format(t=self.transform,
                                            m=self.material)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.transform == other.transform and \
           self.material == other.material:
            return True
        else:
            return False
