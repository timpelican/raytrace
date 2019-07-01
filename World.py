# A world to put objects and lights if __name__ == '__main__':
import Light
import Tuple4
import Sphere
import Transformation


class World(object):
    def __init__(self):
        self.lights = []
        self.objects = []


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
