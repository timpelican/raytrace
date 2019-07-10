# camera
import Matrix
import math


class Camera(object):
    def __init__(self, hsize, vsize, fov):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = fov
        self.transform = Matrix.IdentityMatrix(4)

        # Calculate and store pixel size
        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        self.pixel_size = (self.half_width * 2) / self.hsize
