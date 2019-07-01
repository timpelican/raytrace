# Light sources


class PointLight(object):
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

    def __str__(self):
        return 'PointLight(({p}), ({i}))'.format(p=self.position,
                                                 i=self.intensity)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.position == other.position and \
           self.intensity == other.intensity:
            return True
        else:
            return False
