# Intersections track the t-value for the ray
# and the object it intersected at that t-value

import itertools
import maths


class Intersection(object):
    def __init__(self, t, object):
        self.t = t
        self.object = object

    def __str__(self):
        return '({t}, {o})'.format(t=self.t, o=self.object)

    def __repr__(self):
        return self.__str__()

    def prepare_computations(self, ray):
        # instantiate a data structure for storing some precomputed values
        comps = Computation()
        # copy the intersection's properties, for convenience
        comps.t = self.t
        comps.object = self.object
        # precompute some useful values
        comps.point = ray.position(comps.t)
        comps.eyev = -ray.direction
        comps.normalv = comps.object.normal_at(comps.point)
        if comps.normalv.dot(comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
        else:
            comps.inside = False
        # after computing and (if appropriate) negating
        # the normal vector...
        comps.over_point = comps.point + comps.normalv * maths.EPSILON
        comps.reflectv = ray.direction.reflect(comps.normalv)

        return comps


class Intersections(object):
    def __init__(self, *argv):
        self.data = []
        for arg in argv:
            self.data.append(arg)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def hit(self):
        self.data.sort(key=lambda x: x.t)
        for i in self.data:
            if i.t > 0:
                return i
        return None

    def __str__(self):
        return str(self.data)

    def __add__(self, other):
        i = Intersections()
        for d in itertools.chain(self.data, other.data):
            i.data.append(d)
        return i

    def sort(self):
        self.data.sort(key=lambda x: x.t)
        return self


class Computation(object):
    def __init__(self):
        pass
