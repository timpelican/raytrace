# Visually axis-decorrelated coherent noise algorithm based on the Simplectic
# honeycomb.
#
# After OpenSimplex Noise in Java by Kurt Spencer

import math


class Noise(object):
    STRETCH_CONSTANT_2D = -0.211324865405187    # (1/Math.sqrt(2+1)-1)/2
    SQUISH_CONSTANT_2D = 0.366025403784439      # (Math.sqrt(2+1)-1)/2
    STRETCH_CONSTANT_3D = -1.0 / 6              # (1/Math.sqrt(3+1)-1)/3
    SQUISH_CONSTANT_3D = 1.0 / 3                # (Math.sqrt(3+1)-1)/3
    STRETCH_CONSTANT_4D = -0.138196601125011    # (1/Math.sqrt(4+1)-1)/4
    SQUISH_CONSTANT_4D = 0.309016994374947      # (Math.sqrt(4+1)-1)/4

    NORM_CONSTANT_2D = 47
    NORM_CONSTANT_3D = 103
    NORM_CONSTANT_4D = 30

    DEFAULT_SEED = 0

    # Gradients for 2D. They approximate the directions to the
    # vertices of an octagon from the center.
    gradients2D = [
         5,  2,    2,  5,
        -5,  2,   -2,  5,
         5, -2,    2, -5,
        -5, -2,   -2, -5,
    ]

    # Gradients for 3D. They approximate the directions to the
    # vertices of a rhombicuboctahedron from the center, skewed so
    # that the triangular and square facets can be inscribed inside
    # circles of the same radius.
    gradients3D = [
        -11,  4,  4,     -4,  11,  4,    -4,  4,  11,
         11,  4,  4,      4,  11,  4,     4,  4,  11,
        -11, -4,  4,     -4, -11,  4,    -4, -4,  11,
         11, -4,  4,      4, -11,  4,     4, -4,  11,
        -11,  4, -4,     -4,  11, -4,    -4,  4, -11,
         11,  4, -4,      4,  11, -4,     4,  4, -11,
        -11, -4, -4,     -4, -11, -4,    -4, -4, -11,
         11, -4, -4,      4, -11, -4,     4, -4, -11,
    ]

    @staticmethod
    def fastFloor(x):
        xi = int(x)
        return xi - 1 if x < xi else xi

    def __init__(self, seed=DEFAULT_SEED):
        # Initializes the class using a permutation array generated from a
        # 64-bit seed.
        # Generates a proper permutation (i.e. doesn't merely perform N
        # successive pair swaps on a base array)
        # Uses a simple 64-bit LCG.

        perm = [None] * 256
        permGradIndex3D = [None] * 256
        source = [None] * 256
        for i in range(256):
            source[i] = i
        seed = seed * 6364136223846793005 + 1442695040888963407
        seed = seed * 6364136223846793005 + 1442695040888963407
        seed = seed * 6364136223846793005 + 1442695040888963407
        for i in range(256)[::-1]:
            seed = seed * 6364136223846793005 + 1442695040888963407
            r = int((seed + 31) % (i + 1))
            if (r < 0):
                r += (i + 1)
            perm[i] = source[r]
            permGradIndex3D[i] = int((perm[i] % (len(Noise.gradients3D) / 3))
                                     * 3)
            source[r] = source[i]

        self.perm = perm
        self.permGradIndex3D = permGradIndex3D

    # 2D OpenSimplex Noise.
    def eval2d(self, x, y):

        # Place input coordinates onto grid.
        stretchOffset = (x + y) * Noise.STRETCH_CONSTANT_2D
        xs = x + stretchOffset
        ys = y + stretchOffset

        # Floor to get grid coordinates of rhombus (stretched square)
        # super-cell origin.
        xsb = Noise.fastFloor(xs)
        ysb = Noise.fastFloor(ys)

        # Skew out to get actual coordinates of rhombus origin. We'll need
        # these later.
        squishOffset = (xsb + ysb) * Noise.SQUISH_CONSTANT_2D
        xb = xsb + squishOffset
        yb = ysb + squishOffset

        # Compute grid coordinates relative to rhombus origin.
        xins = xs - xsb
        yins = ys - ysb

        # Sum those together to get a value that determines which region
        # we're in.
        inSum = xins + yins

        # Positions relative to origin point.
        dx0 = x - xb
        dy0 = y - yb

        value = 0

        # Contribution (1,0)
        dx1 = dx0 - 1 - Noise.SQUISH_CONSTANT_2D
        dy1 = dy0 - 0 - Noise.SQUISH_CONSTANT_2D
        attn1 = 2 - dx1 * dx1 - dy1 * dy1
        if (attn1 > 0):
            attn1 *= attn1
            value += attn1 * attn1 * self.extrapolate2(xsb + 1, ysb + 0,
                                                       dx1, dy1)

        # Contribution (0,1)
        dx2 = dx0 - 0 - Noise.SQUISH_CONSTANT_2D
        dy2 = dy0 - 1 - Noise.SQUISH_CONSTANT_2D
        attn2 = 2 - dx2 * dx2 - dy2 * dy2
        if (attn2 > 0):
            attn2 *= attn2
            value += attn2 * attn2 * self.extrapolate2(xsb + 0, ysb + 1,
                                                       dx2, dy2)

        if (inSum <= 1):    # We're inside the triangle (2-Simplex) at (0,0)
            zins = 1 - inSum
            # (0,0) is one of the closest two triangular vertices
            if (zins > xins or zins > yins):
                if (xins > yins):
                    xsv_ext = xsb + 1
                    ysv_ext = ysb - 1
                    dx_ext = dx0 - 1
                    dy_ext = dy0 + 1
                else:
                    xsv_ext = xsb - 1
                    ysv_ext = ysb + 1
                    dx_ext = dx0 + 1
                    dy_ext = dy0 - 1
            else:   # (1,0) and (0,1) are the closest two vertices.
                xsv_ext = xsb + 1
                ysv_ext = ysb + 1
                dx_ext = dx0 - 1 - 2 * Noise.SQUISH_CONSTANT_2D
                dy_ext = dy0 - 1 - 2 * Noise.SQUISH_CONSTANT_2D
        else:   # We're inside the triangle (2-Simplex) at (1,1)
            zins = 2 - inSum
            # (0,0) is one of the closest two triangular vertices
            if (zins < xins or zins < yins):
                if (xins > yins):
                    xsv_ext = xsb + 2
                    ysv_ext = ysb + 0
                    dx_ext = dx0 - 2 - 2 * Noise.SQUISH_CONSTANT_2D
                    dy_ext = dy0 + 0 - 2 * Noise.SQUISH_CONSTANT_2D
                else:
                    xsv_ext = xsb + 0
                    ysv_ext = ysb + 2
                    dx_ext = dx0 + 0 - 2 * Noise.SQUISH_CONSTANT_2D
                    dy_ext = dy0 - 2 - 2 * Noise.SQUISH_CONSTANT_2D
            else:   # (1,0) and (0,1) are the closest two vertices.
                dx_ext = dx0
                dy_ext = dy0
                xsv_ext = xsb
                ysv_ext = ysb
            xsb += 1
            ysb += 1
            dx0 = dx0 - 1 - 2 * Noise.SQUISH_CONSTANT_2D
            dy0 = dy0 - 1 - 2 * Noise.SQUISH_CONSTANT_2D

        # Contribution (0,0) or (1,1)
        attn0 = 2 - dx0 * dx0 - dy0 * dy0
        if (attn0 > 0):
            attn0 *= attn0
            value += attn0 * attn0 * self.extrapolate2(xsb, ysb, dx0, dy0)

        # Extra Vertex
        attn_ext = 2 - dx_ext * dx_ext - dy_ext * dy_ext
        if (attn_ext > 0):
            attn_ext *= attn_ext
            value += attn_ext * attn_ext * \
                self.extrapolate2(xsv_ext, ysv_ext, dx_ext, dy_ext)

        return value / Noise.NORM_CONSTANT_2D

    def extrapolate2(self, xsb, ysb, dx, dy):
        index = self.perm[(self.perm[xsb & 0xFF] + ysb) & 0xFF] & 0x0E
        return Noise.gradients2D[index] * dx + \
            Noise.gradients2D[index + 1] * dy
