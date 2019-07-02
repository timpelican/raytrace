# Intersections track the t-value for the ray
# and the object it intersected at that t-value

import itertools


class Intersection(object):
    def __init__(self, t, object):
        self.t = t
        self.object = object

    def __str__(self):
        return '({t}, {o})'.format(t=self.t, o=self.object)

    def __repr__(self):
        return self.__str__()


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
