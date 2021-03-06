# camera
import Matrix
import math
import Ray
import Tuple4
import Canvas
import sys


class Camera(object):
    def __init__(self, hsize, vsize, fov):
        # TODO: fix so hsize and vsize are ints
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

    def ray_for_pixel(self, px, py):
        # the offset from the edge of the canvas to the pixel's center
        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size
        # the untransformed coordinates of the pixel in world space.
        # (remember that the camera looks toward -z, so +x is to the *left*.)
        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset
        # using the camera matrix, transform the canvas point and the origin,
        # and then compute the ray's direction vector.
        # (remember that the canvas is at z=-1)
        pixel = self.transform.inverse() * Tuple4.Point(world_x, world_y, -1)
        origin = self.transform.inverse() * Tuple4.Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return Ray.Ray(origin, direction)

    # TODO: this is very tacky progress info, we need to come up with
    # something much better.
    def render_world(self, world, verbose=False):
        image = Canvas.Canvas(int(self.hsize), int(self.vsize))
        for y in range(0, int(self.vsize)):
            for x in range(0, int(self.hsize)):
                ray = self.ray_for_pixel(x, y)
                colour = world.colour_at(ray)
                image.write_pixel(x, y, colour)
                if verbose:
                    sys.stdout.write(".")
                    sys.stdout.flush()
            if verbose:
                sys.stdout.write(str(y))
                sys.stdout.write("\n")
                sys.stdout.flush()
        return image
