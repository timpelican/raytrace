# Materials
import Tuple4
import math


class Material(object):
    def __init__(self, colour=Tuple4.Colour(1, 1, 1), ambient=0.1, diffuse=0.9,
                 specular=0.9, shininess=200):
        self.colour = colour
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def __eq__(self, other):
        if self.colour == other.colour and \
           self.ambient == other.ambient and \
           self.diffuse == other.diffuse and \
           self.specular == other.specular and \
           self.shininess == other.shininess:
            return True
        else:
            return False

    def lighting(self, object, light, pos, eye, norm, shadow=False):
        black = Tuple4.Colour(0, 0, 0)

        # Get the point in object space
        opos = object.inverse_transform * pos
        # Check if we have a pattern, otherwise use the inherent colour
        if hasattr(self, "pattern"):
            colour = self.pattern.stripe_at(opos)
        else:
            colour = self.colour
        # combine the surface color with the light's color/intensity
        effective_colour = colour * light.intensity

        # find the direction to the light source
        lightv = (light.position - pos).normalize()

        # compute the ambient contribution
        ambient = effective_colour * self.ambient

        # If we are in shadow, diffuse and specular are both black
        # Test here to avoid an extra calculation below
        if shadow:
            diffuse = black
            specular = black
        else:
            # light_dot_normal represents the cosine of the angle between the
            # light vector and the normal vector. A negative number means the
            # light is on the other side of the surface.
            light_dot_normal = lightv.dot(norm)
            if light_dot_normal < 0:
                diffuse = black
                specular = black
            else:
                # compute the diffuse contribution
                diffuse = effective_colour * self.diffuse * light_dot_normal

                # reflect_dot_eye represents the cosine of the angle between
                # the reflection vector and the eye vector. A negative number
                # means the light reflects away from the eye.
                reflectv = (-lightv).reflect(norm)
                reflect_dot_eye = reflectv.dot(eye)
                if reflect_dot_eye <= 0:
                    specular = black
                else:
                    # compute the specular contribution
                    factor = math.pow(reflect_dot_eye, self.shininess)
                    specular = light.intensity * self.specular * factor

        # Add the three contributions together to get the final shading
        return ambient + diffuse + specular

    def __str__(self):
        return 'Material(({c}), {a}, {d}, {s1}, {s2})'.\
            format(c=self.colour, a=self.ambient, d=self.diffuse,
                   s1=self.specular, s2=self.shininess)

    def __repr__(self):
        return self.__str__()
