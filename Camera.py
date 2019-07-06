# camera
import Matrix


class Camera(object):
    def __init__(self, hsize, vsize, fov):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = fov
        self.transform = Matrix.IdentityMatrix(4)
