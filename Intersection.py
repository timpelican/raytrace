# Intersections track the t-value for the ray
# and the object it intersected at that t-value


class Intersection(object):
    def __init__(self, t, object):
        self.t = t
        self.object = object
