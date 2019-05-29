# Materials
import Tuple4


class Material(object):
    def __init__(self, colour=Tuple4.Colour(1, 1, 1), ambient=0.1, diffuse=0.9,
                 specular=0.9, shininess=200):
        self.colour = colour
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
