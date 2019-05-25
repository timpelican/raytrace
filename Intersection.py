# Intersections track the t-value for the ray
# and the object it intersected at that t-value


class Intersection(object):
    def __init__(self, t, object):
        self.t = t
        self.object = object


class Intersections(object):
    def __init__(self, *argv):
        self.data = []
        for arg in argv:
            self.data.append(arg)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
