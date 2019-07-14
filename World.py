# A world to put objects and lights if __name__ == '__main__':
import Light
import Tuple4
import Sphere
import Transformation
import Intersection
import Ray


class World(object):
    def __init__(self):
        self.lights = []
        self.objects = []

    def intersections(self, ray):
        i = Intersection.Intersections()
        for object in self.objects:
            i += object.intersects(ray)
        return i.sort()

    def shade_hit(self, comp):
        # Start with black
        c = Tuple4.Colour(0, 0, 0)
        # Then add the contribution from each light source
        for l in self.lights:
            s = self.is_shadowed(comp.point, l)
            c += comp.object.material.lighting(l, comp.point, comp.eyev,
                                               comp.normalv, s)
        return c

    def colour_at(self, ray):
        i = self.intersections(ray)
        hit = i.hit()
        if hit:
            comps = hit.prepare_computations(ray)
            return self.shade_hit(comps)
        else:
            return Tuple4.Colour(0, 0, 0)

    # To cope with multiple lights, we need to check if we're in the shadow of
    # a given light
    def is_shadowed(self, p, l):
        v = l.position - p
        distance = v.magnitude()
        direction = v.normalize()
        r = Ray.Ray(p, direction)
        intersections = self.intersections(r)
        h = intersections.hit()
        if h is not None and h.t < distance:
            return True
        else:
            return False


def DefaultWorld():
    w = World()
    w.lights.append(Light.PointLight(Tuple4.Point(-10, 10, -10),
                                     Tuple4.Colour(1, 1, 1)))

    s1 = Sphere.Sphere()
    s1.material.colour = Tuple4.Colour(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2
    w.objects.append(s1)

    s2 = Sphere.Sphere()
    s2.transform = Transformation.Scaling(0.5, 0.5, 0.5)
    w.objects.append(s2)

    return w
