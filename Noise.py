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


	# public OpenSimplexNoise(short[] perm) {
	# 	this.perm = perm
	# 	permGradIndex3D = new short[256]
    #
	# 	for (int i = 0; i < 256; i++) {
	# 		//Since 3D has 24 gradients, simple bitmask won't work, so precompute modulo array.
	# 		permGradIndex3D[i] = (short)((perm[i] % (gradients3D.length / 3)) * 3)
	# 	}
	# }


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

# 	//3D OpenSimplex Noise.
# 	public eval(x, y, z) {
#
# 		//Place input coordinates on simplectic honeycomb.
# 		stretchOffset = (x + y + z) * STRETCH_CONSTANT_3D
# 		xs = x + stretchOffset
# 		ys = y + stretchOffset
# 		zs = z + stretchOffset
#
# 		//Floor to get simplectic honeycomb coordinates of rhombohedron (stretched cube) super-cell origin.
# 		int xsb = fastFloor(xs)
# 		int ysb = fastFloor(ys)
# 		int zsb = fastFloor(zs)
#
# 		//Skew out to get actual coordinates of rhombohedron origin. We'll need these later.
# 		squishOffset = (xsb + ysb + zsb) * SQUISH_CONSTANT_3D
# 		xb = xsb + squishOffset
# 		yb = ysb + squishOffset
# 		zb = zsb + squishOffset
#
# 		//Compute simplectic honeycomb coordinates relative to rhombohedral origin.
# 		xins = xs - xsb
# 		yins = ys - ysb
# 		zins = zs - zsb
#
# 		//Sum those together to get a value that determines which region we're in.
# 		inSum = xins + yins + zins
#
# 		//Positions relative to origin point.
# 		dx0 = x - xb
# 		dy0 = y - yb
# 		dz0 = z - zb
#
# 		//We'll be defining these inside the next block and using them afterwards.
# 		dx_ext0, dy_ext0, dz_ext0
# 		dx_ext1, dy_ext1, dz_ext1
# 		int xsv_ext0, ysv_ext0, zsv_ext0
# 		int xsv_ext1, ysv_ext1, zsv_ext1
#
# 		value = 0
# 		if (inSum <= 1) { //We're inside the tetrahedron (3-Simplex) at (0,0,0)
#
# 			//Determine which two of (0,0,1), (0,1,0), (1,0,0) are closest.
# 			byte aPoint = 0x01
# 			aScore = xins
# 			byte bPoint = 0x02
# 			bScore = yins
# 			if (aScore >= bScore && zins > bScore) {
# 				bScore = zins
# 				bPoint = 0x04
# 			} else if (aScore < bScore && zins > aScore) {
# 				aScore = zins
# 				aPoint = 0x04
# 			}
#
# 			//Now we determine the two lattice points not part of the tetrahedron that may contribute.
# 			//This depends on the closest two tetrahedral vertices, including (0,0,0)
# 			wins = 1 - inSum
# 			if (wins > aScore || wins > bScore) { //(0,0,0) is one of the closest two tetrahedral vertices.
# 				byte c = (bScore > aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
#
# 				if ((c & 0x01) == 0) {
# 					xsv_ext0 = xsb - 1
# 					xsv_ext1 = xsb
# 					dx_ext0 = dx0 + 1
# 					dx_ext1 = dx0
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb + 1
# 					dx_ext0 = dx_ext1 = dx0 - 1
# 				}
#
# 				if ((c & 0x02) == 0) {
# 					ysv_ext0 = ysv_ext1 = ysb
# 					dy_ext0 = dy_ext1 = dy0
# 					if ((c & 0x01) == 0) {
# 						ysv_ext1 -= 1
# 						dy_ext1 += 1
# 					} else {
# 						ysv_ext0 -= 1
# 						dy_ext0 += 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy0 - 1
# 				}
#
# 				if ((c & 0x04) == 0) {
# 					zsv_ext0 = zsb
# 					zsv_ext1 = zsb - 1
# 					dz_ext0 = dz0
# 					dz_ext1 = dz0 + 1
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb + 1
# 					dz_ext0 = dz_ext1 = dz0 - 1
# 				}
# 			} else { //(0,0,0) is not one of the closest two tetrahedral vertices.
# 				byte c = (byte)(aPoint | bPoint); //Our two extra vertices are determined by the closest two.
#
# 				if ((c & 0x01) == 0) {
# 					xsv_ext0 = xsb
# 					xsv_ext1 = xsb - 1
# 					dx_ext0 = dx0 - 2 * SQUISH_CONSTANT_3D
# 					dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb + 1
# 					dx_ext0 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
# 					dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x02) == 0) {
# 					ysv_ext0 = ysb
# 					ysv_ext1 = ysb - 1
# 					dy_ext0 = dy0 - 2 * SQUISH_CONSTANT_3D
# 					dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb + 1
# 					dy_ext0 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
# 					dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x04) == 0) {
# 					zsv_ext0 = zsb
# 					zsv_ext1 = zsb - 1
# 					dz_ext0 = dz0 - 2 * SQUISH_CONSTANT_3D
# 					dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb + 1
# 					dz_ext0 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
# 					dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D
# 				}
# 			}
#
# 			//Contribution (0,0,0)
# 			attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
# 			if (attn0 > 0) {
# 				attn0 *= attn0
# 				value += attn0 * attn0 * extrapolate(xsb + 0, ysb + 0, zsb + 0, dx0, dy0, dz0)
# 			}
#
# 			//Contribution (1,0,0)
# 			dx1 = dx0 - 1 - SQUISH_CONSTANT_3D
# 			dy1 = dy0 - 0 - SQUISH_CONSTANT_3D
# 			dz1 = dz0 - 0 - SQUISH_CONSTANT_3D
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)
# 			}
#
# 			//Contribution (0,1,0)
# 			dx2 = dx0 - 0 - SQUISH_CONSTANT_3D
# 			dy2 = dy0 - 1 - SQUISH_CONSTANT_3D
# 			dz2 = dz1
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)
# 			}
#
# 			//Contribution (0,0,1)
# 			dx3 = dx2
# 			dy3 = dy1
# 			dz3 = dz0 - 1 - SQUISH_CONSTANT_3D
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)
# 			}
# 		} else if (inSum >= 2) { //We're inside the tetrahedron (3-Simplex) at (1,1,1)
#
# 			//Determine which two tetrahedral vertices are the closest, out of (1,1,0), (1,0,1), (0,1,1) but not (1,1,1).
# 			byte aPoint = 0x06
# 			aScore = xins
# 			byte bPoint = 0x05
# 			bScore = yins
# 			if (aScore <= bScore && zins < bScore) {
# 				bScore = zins
# 				bPoint = 0x03
# 			} else if (aScore > bScore && zins < aScore) {
# 				aScore = zins
# 				aPoint = 0x03
# 			}
#
# 			//Now we determine the two lattice points not part of the tetrahedron that may contribute.
# 			//This depends on the closest two tetrahedral vertices, including (1,1,1)
# 			wins = 3 - inSum
# 			if (wins < aScore || wins < bScore) { //(1,1,1) is one of the closest two tetrahedral vertices.
# 				byte c = (bScore < aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
#
# 				if ((c & 0x01) != 0) {
# 					xsv_ext0 = xsb + 2
# 					xsv_ext1 = xsb + 1
# 					dx_ext0 = dx0 - 2 - 3 * SQUISH_CONSTANT_3D
# 					dx_ext1 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb
# 					dx_ext0 = dx_ext1 = dx0 - 3 * SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x02) != 0) {
# 					ysv_ext0 = ysv_ext1 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
# 					if ((c & 0x01) != 0) {
# 						ysv_ext1 += 1
# 						dy_ext1 -= 1
# 					} else {
# 						ysv_ext0 += 1
# 						dy_ext0 -= 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb
# 					dy_ext0 = dy_ext1 = dy0 - 3 * SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x04) != 0) {
# 					zsv_ext0 = zsb + 1
# 					zsv_ext1 = zsb + 2
# 					dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
# 					dz_ext1 = dz0 - 2 - 3 * SQUISH_CONSTANT_3D
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb
# 					dz_ext0 = dz_ext1 = dz0 - 3 * SQUISH_CONSTANT_3D
# 				}
# 			} else { //(1,1,1) is not one of the closest two tetrahedral vertices.
# 				byte c = (byte)(aPoint & bPoint); //Our two extra vertices are determined by the closest two.
#
# 				if ((c & 0x01) != 0) {
# 					xsv_ext0 = xsb + 1
# 					xsv_ext1 = xsb + 2
# 					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
# 					dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb
# 					dx_ext0 = dx0 - SQUISH_CONSTANT_3D
# 					dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x02) != 0) {
# 					ysv_ext0 = ysb + 1
# 					ysv_ext1 = ysb + 2
# 					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
# 					dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb
# 					dy_ext0 = dy0 - SQUISH_CONSTANT_3D
# 					dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
# 				}
#
# 				if ((c & 0x04) != 0) {
# 					zsv_ext0 = zsb + 1
# 					zsv_ext1 = zsb + 2
# 					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
# 					dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb
# 					dz_ext0 = dz0 - SQUISH_CONSTANT_3D
# 					dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
# 				}
# 			}
#
# 			//Contribution (1,1,0)
# 			dx3 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			dy3 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			dz3 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 1, ysb + 1, zsb + 0, dx3, dy3, dz3)
# 			}
#
# 			//Contribution (1,0,1)
# 			dx2 = dx3
# 			dy2 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			dz2 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 1, ysb + 0, zsb + 1, dx2, dy2, dz2)
# 			}
#
# 			//Contribution (0,1,1)
# 			dx1 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			dy1 = dy3
# 			dz1 = dz2
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 0, ysb + 1, zsb + 1, dx1, dy1, dz1)
# 			}
#
# 			//Contribution (1,1,1)
# 			dx0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
# 			dy0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
# 			dz0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
# 			attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
# 			if (attn0 > 0) {
# 				attn0 *= attn0
# 				value += attn0 * attn0 * extrapolate(xsb + 1, ysb + 1, zsb + 1, dx0, dy0, dz0)
# 			}
# 		} else { //We're inside the octahedron (Rectified 3-Simplex) in between.
# 			aScore
# 			byte aPoint
# 			boolean aIsFurtherSide
# 			bScore
# 			byte bPoint
# 			boolean bIsFurtherSide
#
# 			//Decide between point (0,0,1) and (1,1,0) as closest
# 			p1 = xins + yins
# 			if (p1 > 1) {
# 				aScore = p1 - 1
# 				aPoint = 0x03
# 				aIsFurtherSide = true
# 			} else {
# 				aScore = 1 - p1
# 				aPoint = 0x04
# 				aIsFurtherSide = false
# 			}
#
# 			//Decide between point (0,1,0) and (1,0,1) as closest
# 			p2 = xins + zins
# 			if (p2 > 1) {
# 				bScore = p2 - 1
# 				bPoint = 0x05
# 				bIsFurtherSide = true
# 			} else {
# 				bScore = 1 - p2
# 				bPoint = 0x02
# 				bIsFurtherSide = false
# 			}
#
# 			//The closest out of the two (1,0,0) and (0,1,1) will replace the furthest out of the two decided above, if closer.
# 			p3 = yins + zins
# 			if (p3 > 1) {
# 				score = p3 - 1
# 				if (aScore <= bScore && aScore < score) {
# 					aScore = score
# 					aPoint = 0x06
# 					aIsFurtherSide = true
# 				} else if (aScore > bScore && bScore < score) {
# 					bScore = score
# 					bPoint = 0x06
# 					bIsFurtherSide = true
# 				}
# 			} else {
# 				score = 1 - p3
# 				if (aScore <= bScore && aScore < score) {
# 					aScore = score
# 					aPoint = 0x01
# 					aIsFurtherSide = false
# 				} else if (aScore > bScore && bScore < score) {
# 					bScore = score
# 					bPoint = 0x01
# 					bIsFurtherSide = false
# 				}
# 			}
#
# 			//Where each of the two closest points are determines how the extra two vertices are calculated.
# 			if (aIsFurtherSide == bIsFurtherSide) {
# 				if (aIsFurtherSide) { //Both closest points on (1,1,1) side
#
# 					//One of the two extra points is (1,1,1)
# 					dx_ext0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
# 					dy_ext0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
# 					dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
# 					xsv_ext0 = xsb + 1
# 					ysv_ext0 = ysb + 1
# 					zsv_ext0 = zsb + 1
#
# 					//Other extra point is based on the shared axis.
# 					byte c = (byte)(aPoint & bPoint)
# 					if ((c & 0x01) != 0) {
# 						dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb + 2
# 						ysv_ext1 = ysb
# 						zsv_ext1 = zsb
# 					} else if ((c & 0x02) != 0) {
# 						dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb
# 						ysv_ext1 = ysb + 2
# 						zsv_ext1 = zsb
# 					} else {
# 						dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb
# 						ysv_ext1 = ysb
# 						zsv_ext1 = zsb + 2
# 					}
# 				} else {//Both closest points on (0,0,0) side
#
# 					//One of the two extra points is (0,0,0)
# 					dx_ext0 = dx0
# 					dy_ext0 = dy0
# 					dz_ext0 = dz0
# 					xsv_ext0 = xsb
# 					ysv_ext0 = ysb
# 					zsv_ext0 = zsb
#
# 					//Other extra point is based on the omitted axis.
# 					byte c = (byte)(aPoint | bPoint)
# 					if ((c & 0x01) == 0) {
# 						dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb - 1
# 						ysv_ext1 = ysb + 1
# 						zsv_ext1 = zsb + 1
# 					} else if ((c & 0x02) == 0) {
# 						dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb + 1
# 						ysv_ext1 = ysb - 1
# 						zsv_ext1 = zsb + 1
# 					} else {
# 						dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D
# 						dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D
# 						dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D
# 						xsv_ext1 = xsb + 1
# 						ysv_ext1 = ysb + 1
# 						zsv_ext1 = zsb - 1
# 					}
# 				}
# 			} else { //One point on (0,0,0) side, one point on (1,1,1) side
# 				byte c1, c2
# 				if (aIsFurtherSide) {
# 					c1 = aPoint
# 					c2 = bPoint
# 				} else {
# 					c1 = bPoint
# 					c2 = aPoint
# 				}
#
# 				//One contribution is a permutation of (1,1,-1)
# 				if ((c1 & 0x01) == 0) {
# 					dx_ext0 = dx0 + 1 - SQUISH_CONSTANT_3D
# 					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
# 					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
# 					xsv_ext0 = xsb - 1
# 					ysv_ext0 = ysb + 1
# 					zsv_ext0 = zsb + 1
# 				} else if ((c1 & 0x02) == 0) {
# 					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
# 					dy_ext0 = dy0 + 1 - SQUISH_CONSTANT_3D
# 					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
# 					xsv_ext0 = xsb + 1
# 					ysv_ext0 = ysb - 1
# 					zsv_ext0 = zsb + 1
# 				} else {
# 					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
# 					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
# 					dz_ext0 = dz0 + 1 - SQUISH_CONSTANT_3D
# 					xsv_ext0 = xsb + 1
# 					ysv_ext0 = ysb + 1
# 					zsv_ext0 = zsb - 1
# 				}
#
# 				//One contribution is a permutation of (0,0,2)
# 				dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
# 				dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
# 				dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
# 				xsv_ext1 = xsb
# 				ysv_ext1 = ysb
# 				zsv_ext1 = zsb
# 				if ((c2 & 0x01) != 0) {
# 					dx_ext1 -= 2
# 					xsv_ext1 += 2
# 				} else if ((c2 & 0x02) != 0) {
# 					dy_ext1 -= 2
# 					ysv_ext1 += 2
# 				} else {
# 					dz_ext1 -= 2
# 					zsv_ext1 += 2
# 				}
# 			}
#
# 			//Contribution (1,0,0)
# 			dx1 = dx0 - 1 - SQUISH_CONSTANT_3D
# 			dy1 = dy0 - 0 - SQUISH_CONSTANT_3D
# 			dz1 = dz0 - 0 - SQUISH_CONSTANT_3D
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)
# 			}
#
# 			//Contribution (0,1,0)
# 			dx2 = dx0 - 0 - SQUISH_CONSTANT_3D
# 			dy2 = dy0 - 1 - SQUISH_CONSTANT_3D
# 			dz2 = dz1
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)
# 			}
#
# 			//Contribution (0,0,1)
# 			dx3 = dx2
# 			dy3 = dy1
# 			dz3 = dz0 - 1 - SQUISH_CONSTANT_3D
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)
# 			}
#
# 			//Contribution (1,1,0)
# 			dx4 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			dy4 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			dz4 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4
# 			if (attn4 > 0) {
# 				attn4 *= attn4
# 				value += attn4 * attn4 * extrapolate(xsb + 1, ysb + 1, zsb + 0, dx4, dy4, dz4)
# 			}
#
# 			//Contribution (1,0,1)
# 			dx5 = dx4
# 			dy5 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			dz5 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
# 			attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5
# 			if (attn5 > 0) {
# 				attn5 *= attn5
# 				value += attn5 * attn5 * extrapolate(xsb + 1, ysb + 0, zsb + 1, dx5, dy5, dz5)
# 			}
#
# 			//Contribution (0,1,1)
# 			dx6 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D
# 			dy6 = dy4
# 			dz6 = dz5
# 			attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6
# 			if (attn6 > 0) {
# 				attn6 *= attn6
# 				value += attn6 * attn6 * extrapolate(xsb + 0, ysb + 1, zsb + 1, dx6, dy6, dz6)
# 			}
# 		}
#
# 		//First extra vertex
# 		attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0
# 		if (attn_ext0 > 0)
# 		{
# 			attn_ext0 *= attn_ext0
# 			value += attn_ext0 * attn_ext0 * extrapolate(xsv_ext0, ysv_ext0, zsv_ext0, dx_ext0, dy_ext0, dz_ext0)
# 		}
#
# 		//Second extra vertex
# 		attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1
# 		if (attn_ext1 > 0)
# 		{
# 			attn_ext1 *= attn_ext1
# 			value += attn_ext1 * attn_ext1 * extrapolate(xsv_ext1, ysv_ext1, zsv_ext1, dx_ext1, dy_ext1, dz_ext1)
# 		}
#
# 		return value / NORM_CONSTANT_3D
# 	}
#
# 	//4D OpenSimplex Noise.
# 	public eval(x, y, z, w) {
#
# 		//Place input coordinates on simplectic honeycomb.
# 		stretchOffset = (x + y + z + w) * STRETCH_CONSTANT_4D
# 		xs = x + stretchOffset
# 		ys = y + stretchOffset
# 		zs = z + stretchOffset
# 		ws = w + stretchOffset
#
# 		//Floor to get simplectic honeycomb coordinates of rhombo-hypercube super-cell origin.
# 		int xsb = fastFloor(xs)
# 		int ysb = fastFloor(ys)
# 		int zsb = fastFloor(zs)
# 		int wsb = fastFloor(ws)
#
# 		//Skew out to get actual coordinates of stretched rhombo-hypercube origin. We'll need these later.
# 		squishOffset = (xsb + ysb + zsb + wsb) * SQUISH_CONSTANT_4D
# 		xb = xsb + squishOffset
# 		yb = ysb + squishOffset
# 		zb = zsb + squishOffset
# 		wb = wsb + squishOffset
#
# 		//Compute simplectic honeycomb coordinates relative to rhombo-hypercube origin.
# 		xins = xs - xsb
# 		yins = ys - ysb
# 		zins = zs - zsb
# 		wins = ws - wsb
#
# 		//Sum those together to get a value that determines which region we're in.
# 		inSum = xins + yins + zins + wins
#
# 		//Positions relative to origin point.
# 		dx0 = x - xb
# 		dy0 = y - yb
# 		dz0 = z - zb
# 		dw0 = w - wb
#
# 		//We'll be defining these inside the next block and using them afterwards.
# 		dx_ext0, dy_ext0, dz_ext0, dw_ext0
# 		dx_ext1, dy_ext1, dz_ext1, dw_ext1
# 		dx_ext2, dy_ext2, dz_ext2, dw_ext2
# 		int xsv_ext0, ysv_ext0, zsv_ext0, wsv_ext0
# 		int xsv_ext1, ysv_ext1, zsv_ext1, wsv_ext1
# 		int xsv_ext2, ysv_ext2, zsv_ext2, wsv_ext2
#
# 		value = 0
# 		if (inSum <= 1) { //We're inside the pentachoron (4-Simplex) at (0,0,0,0)
#
# 			//Determine which two of (0,0,0,1), (0,0,1,0), (0,1,0,0), (1,0,0,0) are closest.
# 			byte aPoint = 0x01
# 			aScore = xins
# 			byte bPoint = 0x02
# 			bScore = yins
# 			if (aScore >= bScore && zins > bScore) {
# 				bScore = zins
# 				bPoint = 0x04
# 			} else if (aScore < bScore && zins > aScore) {
# 				aScore = zins
# 				aPoint = 0x04
# 			}
# 			if (aScore >= bScore && wins > bScore) {
# 				bScore = wins
# 				bPoint = 0x08
# 			} else if (aScore < bScore && wins > aScore) {
# 				aScore = wins
# 				aPoint = 0x08
# 			}
#
# 			//Now we determine the three lattice points not part of the pentachoron that may contribute.
# 			//This depends on the closest two pentachoron vertices, including (0,0,0,0)
# 			uins = 1 - inSum
# 			if (uins > aScore || uins > bScore) { //(0,0,0,0) is one of the closest two pentachoron vertices.
# 				byte c = (bScore > aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
# 				if ((c & 0x01) == 0) {
# 					xsv_ext0 = xsb - 1
# 					xsv_ext1 = xsv_ext2 = xsb
# 					dx_ext0 = dx0 + 1
# 					dx_ext1 = dx_ext2 = dx0
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb + 1
# 					dx_ext0 = dx_ext1 = dx_ext2 = dx0 - 1
# 				}
#
# 				if ((c & 0x02) == 0) {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
# 					dy_ext0 = dy_ext1 = dy_ext2 = dy0
# 					if ((c & 0x01) == 0x01) {
# 						ysv_ext0 -= 1
# 						dy_ext0 += 1
# 					} else {
# 						ysv_ext1 -= 1
# 						dy_ext1 += 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 1
# 				}
#
# 				if ((c & 0x04) == 0) {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
# 					dz_ext0 = dz_ext1 = dz_ext2 = dz0
# 					if ((c & 0x03) != 0) {
# 						if ((c & 0x03) == 0x03) {
# 							zsv_ext0 -= 1
# 							dz_ext0 += 1
# 						} else {
# 							zsv_ext1 -= 1
# 							dz_ext1 += 1
# 						}
# 					} else {
# 						zsv_ext2 -= 1
# 						dz_ext2 += 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
# 					dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 1
# 				}
#
# 				if ((c & 0x08) == 0) {
# 					wsv_ext0 = wsv_ext1 = wsb
# 					wsv_ext2 = wsb - 1
# 					dw_ext0 = dw_ext1 = dw0
# 					dw_ext2 = dw0 + 1
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb + 1
# 					dw_ext0 = dw_ext1 = dw_ext2 = dw0 - 1
# 				}
# 			} else { //(0,0,0,0) is not one of the closest two pentachoron vertices.
# 				byte c = (byte)(aPoint | bPoint); //Our three extra vertices are determined by the closest two.
#
# 				if ((c & 0x01) == 0) {
# 					xsv_ext0 = xsv_ext2 = xsb
# 					xsv_ext1 = xsb - 1
# 					dx_ext0 = dx0 - 2 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_4D
# 					dx_ext2 = dx0 - SQUISH_CONSTANT_4D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb + 1
# 					dx_ext0 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx_ext2 = dx0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x02) == 0) {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
# 					dy_ext0 = dy0 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext1 = dy_ext2 = dy0 - SQUISH_CONSTANT_4D
# 					if ((c & 0x01) == 0x01) {
# 						ysv_ext1 -= 1
# 						dy_ext1 += 1
# 					} else {
# 						ysv_ext2 -= 1
# 						dy_ext2 += 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
# 					dy_ext0 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext1 = dy_ext2 = dy0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x04) == 0) {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
# 					dz_ext0 = dz0 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext1 = dz_ext2 = dz0 - SQUISH_CONSTANT_4D
# 					if ((c & 0x03) == 0x03) {
# 						zsv_ext1 -= 1
# 						dz_ext1 += 1
# 					} else {
# 						zsv_ext2 -= 1
# 						dz_ext2 += 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
# 					dz_ext0 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext1 = dz_ext2 = dz0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x08) == 0) {
# 					wsv_ext0 = wsv_ext1 = wsb
# 					wsv_ext2 = wsb - 1
# 					dw_ext0 = dw0 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw0 - SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 + 1 - SQUISH_CONSTANT_4D
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb + 1
# 					dw_ext0 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw_ext2 = dw0 - 1 - SQUISH_CONSTANT_4D
# 				}
# 			}
#
# 			//Contribution (0,0,0,0)
# 			attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0 - dw0 * dw0
# 			if (attn0 > 0) {
# 				attn0 *= attn0
# 				value += attn0 * attn0 * extrapolate(xsb + 0, ysb + 0, zsb + 0, wsb + 0, dx0, dy0, dz0, dw0)
# 			}
#
# 			//Contribution (1,0,0,0)
# 			dx1 = dx0 - 1 - SQUISH_CONSTANT_4D
# 			dy1 = dy0 - 0 - SQUISH_CONSTANT_4D
# 			dz1 = dz0 - 0 - SQUISH_CONSTANT_4D
# 			dw1 = dw0 - 0 - SQUISH_CONSTANT_4D
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, wsb + 0, dx1, dy1, dz1, dw1)
# 			}
#
# 			//Contribution (0,1,0,0)
# 			dx2 = dx0 - 0 - SQUISH_CONSTANT_4D
# 			dy2 = dy0 - 1 - SQUISH_CONSTANT_4D
# 			dz2 = dz1
# 			dw2 = dw1
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, wsb + 0, dx2, dy2, dz2, dw2)
# 			}
#
# 			//Contribution (0,0,1,0)
# 			dx3 = dx2
# 			dy3 = dy1
# 			dz3 = dz0 - 1 - SQUISH_CONSTANT_4D
# 			dw3 = dw1
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, wsb + 0, dx3, dy3, dz3, dw3)
# 			}
#
# 			//Contribution (0,0,0,1)
# 			dx4 = dx2
# 			dy4 = dy1
# 			dz4 = dz1
# 			dw4 = dw0 - 1 - SQUISH_CONSTANT_4D
# 			attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
# 			if (attn4 > 0) {
# 				attn4 *= attn4
# 				value += attn4 * attn4 * extrapolate(xsb + 0, ysb + 0, zsb + 0, wsb + 1, dx4, dy4, dz4, dw4)
# 			}
# 		} else if (inSum >= 3) { //We're inside the pentachoron (4-Simplex) at (1,1,1,1)
# 			//Determine which two of (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1) are closest.
# 			byte aPoint = 0x0E
# 			aScore = xins
# 			byte bPoint = 0x0D
# 			bScore = yins
# 			if (aScore <= bScore && zins < bScore) {
# 				bScore = zins
# 				bPoint = 0x0B
# 			} else if (aScore > bScore && zins < aScore) {
# 				aScore = zins
# 				aPoint = 0x0B
# 			}
# 			if (aScore <= bScore && wins < bScore) {
# 				bScore = wins
# 				bPoint = 0x07
# 			} else if (aScore > bScore && wins < aScore) {
# 				aScore = wins
# 				aPoint = 0x07
# 			}
#
# 			//Now we determine the three lattice points not part of the pentachoron that may contribute.
# 			//This depends on the closest two pentachoron vertices, including (0,0,0,0)
# 			uins = 4 - inSum
# 			if (uins < aScore || uins < bScore) { //(1,1,1,1) is one of the closest two pentachoron vertices.
# 				byte c = (bScore < aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
#
# 				if ((c & 0x01) != 0) {
# 					xsv_ext0 = xsb + 2
# 					xsv_ext1 = xsv_ext2 = xsb + 1
# 					dx_ext0 = dx0 - 2 - 4 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx_ext2 = dx0 - 1 - 4 * SQUISH_CONSTANT_4D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb
# 					dx_ext0 = dx_ext1 = dx_ext2 = dx0 - 4 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x02) != 0) {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					if ((c & 0x01) != 0) {
# 						ysv_ext1 += 1
# 						dy_ext1 -= 1
# 					} else {
# 						ysv_ext0 += 1
# 						dy_ext0 -= 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
# 					dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 4 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x04) != 0) {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
# 					dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					if ((c & 0x03) != 0x03) {
# 						if ((c & 0x03) == 0) {
# 							zsv_ext0 += 1
# 							dz_ext0 -= 1
# 						} else {
# 							zsv_ext1 += 1
# 							dz_ext1 -= 1
# 						}
# 					} else {
# 						zsv_ext2 += 1
# 						dz_ext2 -= 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
# 					dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 4 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x08) != 0) {
# 					wsv_ext0 = wsv_ext1 = wsb + 1
# 					wsv_ext2 = wsb + 2
# 					dw_ext0 = dw_ext1 = dw0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 - 2 - 4 * SQUISH_CONSTANT_4D
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb
# 					dw_ext0 = dw_ext1 = dw_ext2 = dw0 - 4 * SQUISH_CONSTANT_4D
# 				}
# 			} else { //(1,1,1,1) is not one of the closest two pentachoron vertices.
# 				byte c = (byte)(aPoint & bPoint); //Our three extra vertices are determined by the closest two.
#
# 				if ((c & 0x01) != 0) {
# 					xsv_ext0 = xsv_ext2 = xsb + 1
# 					xsv_ext1 = xsb + 2
# 					dx_ext0 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx0 - 2 - 3 * SQUISH_CONSTANT_4D
# 					dx_ext2 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb
# 					dx_ext0 = dx0 - 2 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx_ext2 = dx0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x02) != 0) {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
# 					dy_ext0 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext1 = dy_ext2 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					if ((c & 0x01) != 0) {
# 						ysv_ext2 += 1
# 						dy_ext2 -= 1
# 					} else {
# 						ysv_ext1 += 1
# 						dy_ext1 -= 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
# 					dy_ext0 = dy0 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext1 = dy_ext2 = dy0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x04) != 0) {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
# 					dz_ext0 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext1 = dz_ext2 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					if ((c & 0x03) != 0) {
# 						zsv_ext2 += 1
# 						dz_ext2 -= 1
# 					} else {
# 						zsv_ext1 += 1
# 						dz_ext1 -= 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
# 					dz_ext0 = dz0 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext1 = dz_ext2 = dz0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c & 0x08) != 0) {
# 					wsv_ext0 = wsv_ext1 = wsb + 1
# 					wsv_ext2 = wsb + 2
# 					dw_ext0 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 - 2 - 3 * SQUISH_CONSTANT_4D
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb
# 					dw_ext0 = dw0 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw_ext2 = dw0 - 3 * SQUISH_CONSTANT_4D
# 				}
# 			}
#
# 			//Contribution (1,1,1,0)
# 			dx4 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dy4 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dz4 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dw4 = dw0 - 3 * SQUISH_CONSTANT_4D
# 			attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
# 			if (attn4 > 0) {
# 				attn4 *= attn4
# 				value += attn4 * attn4 * extrapolate(xsb + 1, ysb + 1, zsb + 1, wsb + 0, dx4, dy4, dz4, dw4)
# 			}
#
# 			//Contribution (1,1,0,1)
# 			dx3 = dx4
# 			dy3 = dy4
# 			dz3 = dz0 - 3 * SQUISH_CONSTANT_4D
# 			dw3 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 1, ysb + 1, zsb + 0, wsb + 1, dx3, dy3, dz3, dw3)
# 			}
#
# 			//Contribution (1,0,1,1)
# 			dx2 = dx4
# 			dy2 = dy0 - 3 * SQUISH_CONSTANT_4D
# 			dz2 = dz4
# 			dw2 = dw3
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 1, ysb + 0, zsb + 1, wsb + 1, dx2, dy2, dz2, dw2)
# 			}
#
# 			//Contribution (0,1,1,1)
# 			dx1 = dx0 - 3 * SQUISH_CONSTANT_4D
# 			dz1 = dz4
# 			dy1 = dy4
# 			dw1 = dw3
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 0, ysb + 1, zsb + 1, wsb + 1, dx1, dy1, dz1, dw1)
# 			}
#
# 			//Contribution (1,1,1,1)
# 			dx0 = dx0 - 1 - 4 * SQUISH_CONSTANT_4D
# 			dy0 = dy0 - 1 - 4 * SQUISH_CONSTANT_4D
# 			dz0 = dz0 - 1 - 4 * SQUISH_CONSTANT_4D
# 			dw0 = dw0 - 1 - 4 * SQUISH_CONSTANT_4D
# 			attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0 - dw0 * dw0
# 			if (attn0 > 0) {
# 				attn0 *= attn0
# 				value += attn0 * attn0 * extrapolate(xsb + 1, ysb + 1, zsb + 1, wsb + 1, dx0, dy0, dz0, dw0)
# 			}
# 		} else if (inSum <= 2) { //We're inside the first dispentachoron (Rectified 4-Simplex)
# 			aScore
# 			byte aPoint
# 			boolean aIsBiggerSide = true
# 			bScore
# 			byte bPoint
# 			boolean bIsBiggerSide = true
#
# 			//Decide between (1,1,0,0) and (0,0,1,1)
# 			if (xins + yins > zins + wins) {
# 				aScore = xins + yins
# 				aPoint = 0x03
# 			} else {
# 				aScore = zins + wins
# 				aPoint = 0x0C
# 			}
#
# 			//Decide between (1,0,1,0) and (0,1,0,1)
# 			if (xins + zins > yins + wins) {
# 				bScore = xins + zins
# 				bPoint = 0x05
# 			} else {
# 				bScore = yins + wins
# 				bPoint = 0x0A
# 			}
#
# 			//Closer between (1,0,0,1) and (0,1,1,0) will replace the further of a and b, if closer.
# 			if (xins + wins > yins + zins) {
# 				score = xins + wins
# 				if (aScore >= bScore && score > bScore) {
# 					bScore = score
# 					bPoint = 0x09
# 				} else if (aScore < bScore && score > aScore) {
# 					aScore = score
# 					aPoint = 0x09
# 				}
# 			} else {
# 				score = yins + zins
# 				if (aScore >= bScore && score > bScore) {
# 					bScore = score
# 					bPoint = 0x06
# 				} else if (aScore < bScore && score > aScore) {
# 					aScore = score
# 					aPoint = 0x06
# 				}
# 			}
#
# 			//Decide if (1,0,0,0) is closer.
# 			p1 = 2 - inSum + xins
# 			if (aScore >= bScore && p1 > bScore) {
# 				bScore = p1
# 				bPoint = 0x01
# 				bIsBiggerSide = false
# 			} else if (aScore < bScore && p1 > aScore) {
# 				aScore = p1
# 				aPoint = 0x01
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (0,1,0,0) is closer.
# 			p2 = 2 - inSum + yins
# 			if (aScore >= bScore && p2 > bScore) {
# 				bScore = p2
# 				bPoint = 0x02
# 				bIsBiggerSide = false
# 			} else if (aScore < bScore && p2 > aScore) {
# 				aScore = p2
# 				aPoint = 0x02
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (0,0,1,0) is closer.
# 			p3 = 2 - inSum + zins
# 			if (aScore >= bScore && p3 > bScore) {
# 				bScore = p3
# 				bPoint = 0x04
# 				bIsBiggerSide = false
# 			} else if (aScore < bScore && p3 > aScore) {
# 				aScore = p3
# 				aPoint = 0x04
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (0,0,0,1) is closer.
# 			p4 = 2 - inSum + wins
# 			if (aScore >= bScore && p4 > bScore) {
# 				bScore = p4
# 				bPoint = 0x08
# 				bIsBiggerSide = false
# 			} else if (aScore < bScore && p4 > aScore) {
# 				aScore = p4
# 				aPoint = 0x08
# 				aIsBiggerSide = false
# 			}
#
# 			//Where each of the two closest points are determines how the extra three vertices are calculated.
# 			if (aIsBiggerSide == bIsBiggerSide) {
# 				if (aIsBiggerSide) { //Both closest points on the bigger side
# 					byte c1 = (byte)(aPoint | bPoint)
# 					byte c2 = (byte)(aPoint & bPoint)
# 					if ((c1 & 0x01) == 0) {
# 						xsv_ext0 = xsb
# 						xsv_ext1 = xsb - 1
# 						dx_ext0 = dx0 - 3 * SQUISH_CONSTANT_4D
# 						dx_ext1 = dx0 + 1 - 2 * SQUISH_CONSTANT_4D
# 					} else {
# 						xsv_ext0 = xsv_ext1 = xsb + 1
# 						dx_ext0 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						dx_ext1 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c1 & 0x02) == 0) {
# 						ysv_ext0 = ysb
# 						ysv_ext1 = ysb - 1
# 						dy_ext0 = dy0 - 3 * SQUISH_CONSTANT_4D
# 						dy_ext1 = dy0 + 1 - 2 * SQUISH_CONSTANT_4D
# 					} else {
# 						ysv_ext0 = ysv_ext1 = ysb + 1
# 						dy_ext0 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						dy_ext1 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c1 & 0x04) == 0) {
# 						zsv_ext0 = zsb
# 						zsv_ext1 = zsb - 1
# 						dz_ext0 = dz0 - 3 * SQUISH_CONSTANT_4D
# 						dz_ext1 = dz0 + 1 - 2 * SQUISH_CONSTANT_4D
# 					} else {
# 						zsv_ext0 = zsv_ext1 = zsb + 1
# 						dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						dz_ext1 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c1 & 0x08) == 0) {
# 						wsv_ext0 = wsb
# 						wsv_ext1 = wsb - 1
# 						dw_ext0 = dw0 - 3 * SQUISH_CONSTANT_4D
# 						dw_ext1 = dw0 + 1 - 2 * SQUISH_CONSTANT_4D
# 					} else {
# 						wsv_ext0 = wsv_ext1 = wsb + 1
# 						dw_ext0 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						dw_ext1 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					}
#
# 					//One combination is a permutation of (0,0,0,2) based on c2
# 					xsv_ext2 = xsb
# 					ysv_ext2 = ysb
# 					zsv_ext2 = zsb
# 					wsv_ext2 = wsb
# 					dx_ext2 = dx0 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext2 = dy0 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext2 = dz0 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 - 2 * SQUISH_CONSTANT_4D
# 					if ((c2 & 0x01) != 0) {
# 						xsv_ext2 += 2
# 						dx_ext2 -= 2
# 					} else if ((c2 & 0x02) != 0) {
# 						ysv_ext2 += 2
# 						dy_ext2 -= 2
# 					} else if ((c2 & 0x04) != 0) {
# 						zsv_ext2 += 2
# 						dz_ext2 -= 2
# 					} else {
# 						wsv_ext2 += 2
# 						dw_ext2 -= 2
# 					}
#
# 				} else { //Both closest points on the smaller side
# 					//One of the two extra points is (0,0,0,0)
# 					xsv_ext2 = xsb
# 					ysv_ext2 = ysb
# 					zsv_ext2 = zsb
# 					wsv_ext2 = wsb
# 					dx_ext2 = dx0
# 					dy_ext2 = dy0
# 					dz_ext2 = dz0
# 					dw_ext2 = dw0
#
# 					//Other two points are based on the omitted axes.
# 					byte c = (byte)(aPoint | bPoint)
#
# 					if ((c & 0x01) == 0) {
# 						xsv_ext0 = xsb - 1
# 						xsv_ext1 = xsb
# 						dx_ext0 = dx0 + 1 - SQUISH_CONSTANT_4D
# 						dx_ext1 = dx0 - SQUISH_CONSTANT_4D
# 					} else {
# 						xsv_ext0 = xsv_ext1 = xsb + 1
# 						dx_ext0 = dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x02) == 0) {
# 						ysv_ext0 = ysv_ext1 = ysb
# 						dy_ext0 = dy_ext1 = dy0 - SQUISH_CONSTANT_4D
# 						if ((c & 0x01) == 0x01)
# 						{
# 							ysv_ext0 -= 1
# 							dy_ext0 += 1
# 						} else {
# 							ysv_ext1 -= 1
# 							dy_ext1 += 1
# 						}
# 					} else {
# 						ysv_ext0 = ysv_ext1 = ysb + 1
# 						dy_ext0 = dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x04) == 0) {
# 						zsv_ext0 = zsv_ext1 = zsb
# 						dz_ext0 = dz_ext1 = dz0 - SQUISH_CONSTANT_4D
# 						if ((c & 0x03) == 0x03)
# 						{
# 							zsv_ext0 -= 1
# 							dz_ext0 += 1
# 						} else {
# 							zsv_ext1 -= 1
# 							dz_ext1 += 1
# 						}
# 					} else {
# 						zsv_ext0 = zsv_ext1 = zsb + 1
# 						dz_ext0 = dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x08) == 0)
# 					{
# 						wsv_ext0 = wsb
# 						wsv_ext1 = wsb - 1
# 						dw_ext0 = dw0 - SQUISH_CONSTANT_4D
# 						dw_ext1 = dw0 + 1 - SQUISH_CONSTANT_4D
# 					} else {
# 						wsv_ext0 = wsv_ext1 = wsb + 1
# 						dw_ext0 = dw_ext1 = dw0 - 1 - SQUISH_CONSTANT_4D
# 					}
#
# 				}
# 			} else { //One point on each "side"
# 				byte c1, c2
# 				if (aIsBiggerSide) {
# 					c1 = aPoint
# 					c2 = bPoint
# 				} else {
# 					c1 = bPoint
# 					c2 = aPoint
# 				}
#
# 				//Two contributions are the bigger-sided point with each 0 replaced with -1.
# 				if ((c1 & 0x01) == 0) {
# 					xsv_ext0 = xsb - 1
# 					xsv_ext1 = xsb
# 					dx_ext0 = dx0 + 1 - SQUISH_CONSTANT_4D
# 					dx_ext1 = dx0 - SQUISH_CONSTANT_4D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb + 1
# 					dx_ext0 = dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x02) == 0) {
# 					ysv_ext0 = ysv_ext1 = ysb
# 					dy_ext0 = dy_ext1 = dy0 - SQUISH_CONSTANT_4D
# 					if ((c1 & 0x01) == 0x01) {
# 						ysv_ext0 -= 1
# 						dy_ext0 += 1
# 					} else {
# 						ysv_ext1 -= 1
# 						dy_ext1 += 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x04) == 0) {
# 					zsv_ext0 = zsv_ext1 = zsb
# 					dz_ext0 = dz_ext1 = dz0 - SQUISH_CONSTANT_4D
# 					if ((c1 & 0x03) == 0x03) {
# 						zsv_ext0 -= 1
# 						dz_ext0 += 1
# 					} else {
# 						zsv_ext1 -= 1
# 						dz_ext1 += 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb + 1
# 					dz_ext0 = dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x08) == 0) {
# 					wsv_ext0 = wsb
# 					wsv_ext1 = wsb - 1
# 					dw_ext0 = dw0 - SQUISH_CONSTANT_4D
# 					dw_ext1 = dw0 + 1 - SQUISH_CONSTANT_4D
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsb + 1
# 					dw_ext0 = dw_ext1 = dw0 - 1 - SQUISH_CONSTANT_4D
# 				}
#
# 				//One contribution is a permutation of (0,0,0,2) based on the smaller-sided point
# 				xsv_ext2 = xsb
# 				ysv_ext2 = ysb
# 				zsv_ext2 = zsb
# 				wsv_ext2 = wsb
# 				dx_ext2 = dx0 - 2 * SQUISH_CONSTANT_4D
# 				dy_ext2 = dy0 - 2 * SQUISH_CONSTANT_4D
# 				dz_ext2 = dz0 - 2 * SQUISH_CONSTANT_4D
# 				dw_ext2 = dw0 - 2 * SQUISH_CONSTANT_4D
# 				if ((c2 & 0x01) != 0) {
# 					xsv_ext2 += 2
# 					dx_ext2 -= 2
# 				} else if ((c2 & 0x02) != 0) {
# 					ysv_ext2 += 2
# 					dy_ext2 -= 2
# 				} else if ((c2 & 0x04) != 0) {
# 					zsv_ext2 += 2
# 					dz_ext2 -= 2
# 				} else {
# 					wsv_ext2 += 2
# 					dw_ext2 -= 2
# 				}
# 			}
#
# 			//Contribution (1,0,0,0)
# 			dx1 = dx0 - 1 - SQUISH_CONSTANT_4D
# 			dy1 = dy0 - 0 - SQUISH_CONSTANT_4D
# 			dz1 = dz0 - 0 - SQUISH_CONSTANT_4D
# 			dw1 = dw0 - 0 - SQUISH_CONSTANT_4D
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, wsb + 0, dx1, dy1, dz1, dw1)
# 			}
#
# 			//Contribution (0,1,0,0)
# 			dx2 = dx0 - 0 - SQUISH_CONSTANT_4D
# 			dy2 = dy0 - 1 - SQUISH_CONSTANT_4D
# 			dz2 = dz1
# 			dw2 = dw1
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, wsb + 0, dx2, dy2, dz2, dw2)
# 			}
#
# 			//Contribution (0,0,1,0)
# 			dx3 = dx2
# 			dy3 = dy1
# 			dz3 = dz0 - 1 - SQUISH_CONSTANT_4D
# 			dw3 = dw1
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, wsb + 0, dx3, dy3, dz3, dw3)
# 			}
#
# 			//Contribution (0,0,0,1)
# 			dx4 = dx2
# 			dy4 = dy1
# 			dz4 = dz1
# 			dw4 = dw0 - 1 - SQUISH_CONSTANT_4D
# 			attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
# 			if (attn4 > 0) {
# 				attn4 *= attn4
# 				value += attn4 * attn4 * extrapolate(xsb + 0, ysb + 0, zsb + 0, wsb + 1, dx4, dy4, dz4, dw4)
# 			}
#
# 			//Contribution (1,1,0,0)
# 			dx5 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy5 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz5 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw5 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5 - dw5 * dw5
# 			if (attn5 > 0) {
# 				attn5 *= attn5
# 				value += attn5 * attn5 * extrapolate(xsb + 1, ysb + 1, zsb + 0, wsb + 0, dx5, dy5, dz5, dw5)
# 			}
#
# 			//Contribution (1,0,1,0)
# 			dx6 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy6 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz6 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw6 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6 - dw6 * dw6
# 			if (attn6 > 0) {
# 				attn6 *= attn6
# 				value += attn6 * attn6 * extrapolate(xsb + 1, ysb + 0, zsb + 1, wsb + 0, dx6, dy6, dz6, dw6)
# 			}
#
# 			//Contribution (1,0,0,1)
# 			dx7 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy7 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz7 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw7 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn7 = 2 - dx7 * dx7 - dy7 * dy7 - dz7 * dz7 - dw7 * dw7
# 			if (attn7 > 0) {
# 				attn7 *= attn7
# 				value += attn7 * attn7 * extrapolate(xsb + 1, ysb + 0, zsb + 0, wsb + 1, dx7, dy7, dz7, dw7)
# 			}
#
# 			//Contribution (0,1,1,0)
# 			dx8 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy8 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz8 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw8 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn8 = 2 - dx8 * dx8 - dy8 * dy8 - dz8 * dz8 - dw8 * dw8
# 			if (attn8 > 0) {
# 				attn8 *= attn8
# 				value += attn8 * attn8 * extrapolate(xsb + 0, ysb + 1, zsb + 1, wsb + 0, dx8, dy8, dz8, dw8)
# 			}
#
# 			//Contribution (0,1,0,1)
# 			dx9 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy9 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz9 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw9 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn9 = 2 - dx9 * dx9 - dy9 * dy9 - dz9 * dz9 - dw9 * dw9
# 			if (attn9 > 0) {
# 				attn9 *= attn9
# 				value += attn9 * attn9 * extrapolate(xsb + 0, ysb + 1, zsb + 0, wsb + 1, dx9, dy9, dz9, dw9)
# 			}
#
# 			//Contribution (0,0,1,1)
# 			dx10 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy10 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz10 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw10 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn10 = 2 - dx10 * dx10 - dy10 * dy10 - dz10 * dz10 - dw10 * dw10
# 			if (attn10 > 0) {
# 				attn10 *= attn10
# 				value += attn10 * attn10 * extrapolate(xsb + 0, ysb + 0, zsb + 1, wsb + 1, dx10, dy10, dz10, dw10)
# 			}
# 		} else { //We're inside the second dispentachoron (Rectified 4-Simplex)
# 			aScore
# 			byte aPoint
# 			boolean aIsBiggerSide = true
# 			bScore
# 			byte bPoint
# 			boolean bIsBiggerSide = true
#
# 			//Decide between (0,0,1,1) and (1,1,0,0)
# 			if (xins + yins < zins + wins) {
# 				aScore = xins + yins
# 				aPoint = 0x0C
# 			} else {
# 				aScore = zins + wins
# 				aPoint = 0x03
# 			}
#
# 			//Decide between (0,1,0,1) and (1,0,1,0)
# 			if (xins + zins < yins + wins) {
# 				bScore = xins + zins
# 				bPoint = 0x0A
# 			} else {
# 				bScore = yins + wins
# 				bPoint = 0x05
# 			}
#
# 			//Closer between (0,1,1,0) and (1,0,0,1) will replace the further of a and b, if closer.
# 			if (xins + wins < yins + zins) {
# 				score = xins + wins
# 				if (aScore <= bScore && score < bScore) {
# 					bScore = score
# 					bPoint = 0x06
# 				} else if (aScore > bScore && score < aScore) {
# 					aScore = score
# 					aPoint = 0x06
# 				}
# 			} else {
# 				score = yins + zins
# 				if (aScore <= bScore && score < bScore) {
# 					bScore = score
# 					bPoint = 0x09
# 				} else if (aScore > bScore && score < aScore) {
# 					aScore = score
# 					aPoint = 0x09
# 				}
# 			}
#
# 			//Decide if (0,1,1,1) is closer.
# 			p1 = 3 - inSum + xins
# 			if (aScore <= bScore && p1 < bScore) {
# 				bScore = p1
# 				bPoint = 0x0E
# 				bIsBiggerSide = false
# 			} else if (aScore > bScore && p1 < aScore) {
# 				aScore = p1
# 				aPoint = 0x0E
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (1,0,1,1) is closer.
# 			p2 = 3 - inSum + yins
# 			if (aScore <= bScore && p2 < bScore) {
# 				bScore = p2
# 				bPoint = 0x0D
# 				bIsBiggerSide = false
# 			} else if (aScore > bScore && p2 < aScore) {
# 				aScore = p2
# 				aPoint = 0x0D
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (1,1,0,1) is closer.
# 			p3 = 3 - inSum + zins
# 			if (aScore <= bScore && p3 < bScore) {
# 				bScore = p3
# 				bPoint = 0x0B
# 				bIsBiggerSide = false
# 			} else if (aScore > bScore && p3 < aScore) {
# 				aScore = p3
# 				aPoint = 0x0B
# 				aIsBiggerSide = false
# 			}
#
# 			//Decide if (1,1,1,0) is closer.
# 			p4 = 3 - inSum + wins
# 			if (aScore <= bScore && p4 < bScore) {
# 				bScore = p4
# 				bPoint = 0x07
# 				bIsBiggerSide = false
# 			} else if (aScore > bScore && p4 < aScore) {
# 				aScore = p4
# 				aPoint = 0x07
# 				aIsBiggerSide = false
# 			}
#
# 			//Where each of the two closest points are determines how the extra three vertices are calculated.
# 			if (aIsBiggerSide == bIsBiggerSide) {
# 				if (aIsBiggerSide) { //Both closest points on the bigger side
# 					byte c1 = (byte)(aPoint & bPoint)
# 					byte c2 = (byte)(aPoint | bPoint)
#
# 					//Two contributions are permutations of (0,0,0,1) and (0,0,0,2) based on c1
# 					xsv_ext0 = xsv_ext1 = xsb
# 					ysv_ext0 = ysv_ext1 = ysb
# 					zsv_ext0 = zsv_ext1 = zsb
# 					wsv_ext0 = wsv_ext1 = wsb
# 					dx_ext0 = dx0 - SQUISH_CONSTANT_4D
# 					dy_ext0 = dy0 - SQUISH_CONSTANT_4D
# 					dz_ext0 = dz0 - SQUISH_CONSTANT_4D
# 					dw_ext0 = dw0 - SQUISH_CONSTANT_4D
# 					dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw0 - 2 * SQUISH_CONSTANT_4D
# 					if ((c1 & 0x01) != 0) {
# 						xsv_ext0 += 1
# 						dx_ext0 -= 1
# 						xsv_ext1 += 2
# 						dx_ext1 -= 2
# 					} else if ((c1 & 0x02) != 0) {
# 						ysv_ext0 += 1
# 						dy_ext0 -= 1
# 						ysv_ext1 += 2
# 						dy_ext1 -= 2
# 					} else if ((c1 & 0x04) != 0) {
# 						zsv_ext0 += 1
# 						dz_ext0 -= 1
# 						zsv_ext1 += 2
# 						dz_ext1 -= 2
# 					} else {
# 						wsv_ext0 += 1
# 						dw_ext0 -= 1
# 						wsv_ext1 += 2
# 						dw_ext1 -= 2
# 					}
#
# 					//One contribution is a permutation of (1,1,1,-1) based on c2
# 					xsv_ext2 = xsb + 1
# 					ysv_ext2 = ysb + 1
# 					zsv_ext2 = zsb + 1
# 					wsv_ext2 = wsb + 1
# 					dx_ext2 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dy_ext2 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dz_ext2 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 					if ((c2 & 0x01) == 0) {
# 						xsv_ext2 -= 2
# 						dx_ext2 += 2
# 					} else if ((c2 & 0x02) == 0) {
# 						ysv_ext2 -= 2
# 						dy_ext2 += 2
# 					} else if ((c2 & 0x04) == 0) {
# 						zsv_ext2 -= 2
# 						dz_ext2 += 2
# 					} else {
# 						wsv_ext2 -= 2
# 						dw_ext2 += 2
# 					}
# 				} else { //Both closest points on the smaller side
# 					//One of the two extra points is (1,1,1,1)
# 					xsv_ext2 = xsb + 1
# 					ysv_ext2 = ysb + 1
# 					zsv_ext2 = zsb + 1
# 					wsv_ext2 = wsb + 1
# 					dx_ext2 = dx0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					dy_ext2 = dy0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					dz_ext2 = dz0 - 1 - 4 * SQUISH_CONSTANT_4D
# 					dw_ext2 = dw0 - 1 - 4 * SQUISH_CONSTANT_4D
#
# 					//Other two points are based on the shared axes.
# 					byte c = (byte)(aPoint & bPoint)
#
# 					if ((c & 0x01) != 0) {
# 						xsv_ext0 = xsb + 2
# 						xsv_ext1 = xsb + 1
# 						dx_ext0 = dx0 - 2 - 3 * SQUISH_CONSTANT_4D
# 						dx_ext1 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					} else {
# 						xsv_ext0 = xsv_ext1 = xsb
# 						dx_ext0 = dx_ext1 = dx0 - 3 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x02) != 0) {
# 						ysv_ext0 = ysv_ext1 = ysb + 1
# 						dy_ext0 = dy_ext1 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						if ((c & 0x01) == 0)
# 						{
# 							ysv_ext0 += 1
# 							dy_ext0 -= 1
# 						} else {
# 							ysv_ext1 += 1
# 							dy_ext1 -= 1
# 						}
# 					} else {
# 						ysv_ext0 = ysv_ext1 = ysb
# 						dy_ext0 = dy_ext1 = dy0 - 3 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x04) != 0) {
# 						zsv_ext0 = zsv_ext1 = zsb + 1
# 						dz_ext0 = dz_ext1 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						if ((c & 0x03) == 0)
# 						{
# 							zsv_ext0 += 1
# 							dz_ext0 -= 1
# 						} else {
# 							zsv_ext1 += 1
# 							dz_ext1 -= 1
# 						}
# 					} else {
# 						zsv_ext0 = zsv_ext1 = zsb
# 						dz_ext0 = dz_ext1 = dz0 - 3 * SQUISH_CONSTANT_4D
# 					}
#
# 					if ((c & 0x08) != 0)
# 					{
# 						wsv_ext0 = wsb + 1
# 						wsv_ext1 = wsb + 2
# 						dw_ext0 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 						dw_ext1 = dw0 - 2 - 3 * SQUISH_CONSTANT_4D
# 					} else {
# 						wsv_ext0 = wsv_ext1 = wsb
# 						dw_ext0 = dw_ext1 = dw0 - 3 * SQUISH_CONSTANT_4D
# 					}
# 				}
# 			} else { //One point on each "side"
# 				byte c1, c2
# 				if (aIsBiggerSide) {
# 					c1 = aPoint
# 					c2 = bPoint
# 				} else {
# 					c1 = bPoint
# 					c2 = aPoint
# 				}
#
# 				//Two contributions are the bigger-sided point with each 1 replaced with 2.
# 				if ((c1 & 0x01) != 0) {
# 					xsv_ext0 = xsb + 2
# 					xsv_ext1 = xsb + 1
# 					dx_ext0 = dx0 - 2 - 3 * SQUISH_CONSTANT_4D
# 					dx_ext1 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 				} else {
# 					xsv_ext0 = xsv_ext1 = xsb
# 					dx_ext0 = dx_ext1 = dx0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x02) != 0) {
# 					ysv_ext0 = ysv_ext1 = ysb + 1
# 					dy_ext0 = dy_ext1 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					if ((c1 & 0x01) == 0) {
# 						ysv_ext0 += 1
# 						dy_ext0 -= 1
# 					} else {
# 						ysv_ext1 += 1
# 						dy_ext1 -= 1
# 					}
# 				} else {
# 					ysv_ext0 = ysv_ext1 = ysb
# 					dy_ext0 = dy_ext1 = dy0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x04) != 0) {
# 					zsv_ext0 = zsv_ext1 = zsb + 1
# 					dz_ext0 = dz_ext1 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					if ((c1 & 0x03) == 0) {
# 						zsv_ext0 += 1
# 						dz_ext0 -= 1
# 					} else {
# 						zsv_ext1 += 1
# 						dz_ext1 -= 1
# 					}
# 				} else {
# 					zsv_ext0 = zsv_ext1 = zsb
# 					dz_ext0 = dz_ext1 = dz0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				if ((c1 & 0x08) != 0) {
# 					wsv_ext0 = wsb + 1
# 					wsv_ext1 = wsb + 2
# 					dw_ext0 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 					dw_ext1 = dw0 - 2 - 3 * SQUISH_CONSTANT_4D
# 				} else {
# 					wsv_ext0 = wsv_ext1 = wsb
# 					dw_ext0 = dw_ext1 = dw0 - 3 * SQUISH_CONSTANT_4D
# 				}
#
# 				//One contribution is a permutation of (1,1,1,-1) based on the smaller-sided point
# 				xsv_ext2 = xsb + 1
# 				ysv_ext2 = ysb + 1
# 				zsv_ext2 = zsb + 1
# 				wsv_ext2 = wsb + 1
# 				dx_ext2 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 				dy_ext2 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 				dz_ext2 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 				dw_ext2 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 				if ((c2 & 0x01) == 0) {
# 					xsv_ext2 -= 2
# 					dx_ext2 += 2
# 				} else if ((c2 & 0x02) == 0) {
# 					ysv_ext2 -= 2
# 					dy_ext2 += 2
# 				} else if ((c2 & 0x04) == 0) {
# 					zsv_ext2 -= 2
# 					dz_ext2 += 2
# 				} else {
# 					wsv_ext2 -= 2
# 					dw_ext2 += 2
# 				}
# 			}
#
# 			//Contribution (1,1,1,0)
# 			dx4 = dx0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dy4 = dy0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dz4 = dz0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			dw4 = dw0 - 3 * SQUISH_CONSTANT_4D
# 			attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
# 			if (attn4 > 0) {
# 				attn4 *= attn4
# 				value += attn4 * attn4 * extrapolate(xsb + 1, ysb + 1, zsb + 1, wsb + 0, dx4, dy4, dz4, dw4)
# 			}
#
# 			//Contribution (1,1,0,1)
# 			dx3 = dx4
# 			dy3 = dy4
# 			dz3 = dz0 - 3 * SQUISH_CONSTANT_4D
# 			dw3 = dw0 - 1 - 3 * SQUISH_CONSTANT_4D
# 			attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
# 			if (attn3 > 0) {
# 				attn3 *= attn3
# 				value += attn3 * attn3 * extrapolate(xsb + 1, ysb + 1, zsb + 0, wsb + 1, dx3, dy3, dz3, dw3)
# 			}
#
# 			//Contribution (1,0,1,1)
# 			dx2 = dx4
# 			dy2 = dy0 - 3 * SQUISH_CONSTANT_4D
# 			dz2 = dz4
# 			dw2 = dw3
# 			attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
# 			if (attn2 > 0) {
# 				attn2 *= attn2
# 				value += attn2 * attn2 * extrapolate(xsb + 1, ysb + 0, zsb + 1, wsb + 1, dx2, dy2, dz2, dw2)
# 			}
#
# 			//Contribution (0,1,1,1)
# 			dx1 = dx0 - 3 * SQUISH_CONSTANT_4D
# 			dz1 = dz4
# 			dy1 = dy4
# 			dw1 = dw3
# 			attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
# 			if (attn1 > 0) {
# 				attn1 *= attn1
# 				value += attn1 * attn1 * extrapolate(xsb + 0, ysb + 1, zsb + 1, wsb + 1, dx1, dy1, dz1, dw1)
# 			}
#
# 			//Contribution (1,1,0,0)
# 			dx5 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy5 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz5 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw5 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5 - dw5 * dw5
# 			if (attn5 > 0) {
# 				attn5 *= attn5
# 				value += attn5 * attn5 * extrapolate(xsb + 1, ysb + 1, zsb + 0, wsb + 0, dx5, dy5, dz5, dw5)
# 			}
#
# 			//Contribution (1,0,1,0)
# 			dx6 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy6 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz6 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw6 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6 - dw6 * dw6
# 			if (attn6 > 0) {
# 				attn6 *= attn6
# 				value += attn6 * attn6 * extrapolate(xsb + 1, ysb + 0, zsb + 1, wsb + 0, dx6, dy6, dz6, dw6)
# 			}
#
# 			//Contribution (1,0,0,1)
# 			dx7 = dx0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dy7 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz7 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw7 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn7 = 2 - dx7 * dx7 - dy7 * dy7 - dz7 * dz7 - dw7 * dw7
# 			if (attn7 > 0) {
# 				attn7 *= attn7
# 				value += attn7 * attn7 * extrapolate(xsb + 1, ysb + 0, zsb + 0, wsb + 1, dx7, dy7, dz7, dw7)
# 			}
#
# 			//Contribution (0,1,1,0)
# 			dx8 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy8 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz8 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw8 = dw0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			attn8 = 2 - dx8 * dx8 - dy8 * dy8 - dz8 * dz8 - dw8 * dw8
# 			if (attn8 > 0) {
# 				attn8 *= attn8
# 				value += attn8 * attn8 * extrapolate(xsb + 0, ysb + 1, zsb + 1, wsb + 0, dx8, dy8, dz8, dw8)
# 			}
#
# 			//Contribution (0,1,0,1)
# 			dx9 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy9 = dy0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dz9 = dz0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dw9 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn9 = 2 - dx9 * dx9 - dy9 * dy9 - dz9 * dz9 - dw9 * dw9
# 			if (attn9 > 0) {
# 				attn9 *= attn9
# 				value += attn9 * attn9 * extrapolate(xsb + 0, ysb + 1, zsb + 0, wsb + 1, dx9, dy9, dz9, dw9)
# 			}
#
# 			//Contribution (0,0,1,1)
# 			dx10 = dx0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dy10 = dy0 - 0 - 2 * SQUISH_CONSTANT_4D
# 			dz10 = dz0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			dw10 = dw0 - 1 - 2 * SQUISH_CONSTANT_4D
# 			attn10 = 2 - dx10 * dx10 - dy10 * dy10 - dz10 * dz10 - dw10 * dw10
# 			if (attn10 > 0) {
# 				attn10 *= attn10
# 				value += attn10 * attn10 * extrapolate(xsb + 0, ysb + 0, zsb + 1, wsb + 1, dx10, dy10, dz10, dw10)
# 			}
# 		}
#
# 		//First extra vertex
# 		attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0 - dw_ext0 * dw_ext0
# 		if (attn_ext0 > 0)
# 		{
# 			attn_ext0 *= attn_ext0
# 			value += attn_ext0 * attn_ext0 * extrapolate(xsv_ext0, ysv_ext0, zsv_ext0, wsv_ext0, dx_ext0, dy_ext0, dz_ext0, dw_ext0)
# 		}
#
# 		//Second extra vertex
# 		attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1 - dw_ext1 * dw_ext1
# 		if (attn_ext1 > 0)
# 		{
# 			attn_ext1 *= attn_ext1
# 			value += attn_ext1 * attn_ext1 * extrapolate(xsv_ext1, ysv_ext1, zsv_ext1, wsv_ext1, dx_ext1, dy_ext1, dz_ext1, dw_ext1)
# 		}
#
# 		//Third extra vertex
# 		attn_ext2 = 2 - dx_ext2 * dx_ext2 - dy_ext2 * dy_ext2 - dz_ext2 * dz_ext2 - dw_ext2 * dw_ext2
# 		if (attn_ext2 > 0)
# 		{
# 			attn_ext2 *= attn_ext2
# 			value += attn_ext2 * attn_ext2 * extrapolate(xsv_ext2, ysv_ext2, zsv_ext2, wsv_ext2, dx_ext2, dy_ext2, dz_ext2, dw_ext2)
# 		}
#
# 		return value / NORM_CONSTANT_4D
# 	}
#

    def extrapolate2(self, xsb, ysb, dx, dy):
        index = self.perm[(self.perm[xsb & 0xFF] + ysb) & 0xFF] & 0x0E
        return Noise.gradients2D[index] * dx + \
            Noise.gradients2D[index + 1] * dy


# 	private extrapolate(int xsb, int ysb, int zsb, dx, dy, dz)
# 	{
# 		int index = permGradIndex3D[(perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF]
# 		return gradients3D[index] * dx
# 			+ gradients3D[index + 1] * dy
# 			+ gradients3D[index + 2] * dz
# 	}
#
# 	private extrapolate(int xsb, int ysb, int zsb, int wsb, dx, dy, dz, dw)
# 	{
# 		int index = perm[(perm[(perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF] + wsb) & 0xFF] & 0xFC
# 		return gradients4D[index] * dx
# 			+ gradients4D[index + 1] * dy
# 			+ gradients4D[index + 2] * dz
# 			+ gradients4D[index + 3] * dw
# 	}
#
#
    #
    # 	//Gradients for 4D. They approximate the directions to the
    # 	//vertices of a disprismatotesseractihexadecachoron from the center,
    # 	//skewed so that the tetrahedral and cubic facets can be inscribed inside
    # 	//spheres of the same radius.
    # 	private static byte[] gradients4D = new byte[] {
    # 	     3,  1,  1,  1,      1,  3,  1,  1,      1,  1,  3,  1,      1,  1,  1,  3,
    # 	    -3,  1,  1,  1,     -1,  3,  1,  1,     -1,  1,  3,  1,     -1,  1,  1,  3,
    # 	     3, -1,  1,  1,      1, -3,  1,  1,      1, -1,  3,  1,      1, -1,  1,  3,
    # 	    -3, -1,  1,  1,     -1, -3,  1,  1,     -1, -1,  3,  1,     -1, -1,  1,  3,
    # 	     3,  1, -1,  1,      1,  3, -1,  1,      1,  1, -3,  1,      1,  1, -1,  3,
    # 	    -3,  1, -1,  1,     -1,  3, -1,  1,     -1,  1, -3,  1,     -1,  1, -1,  3,
    # 	     3, -1, -1,  1,      1, -3, -1,  1,      1, -1, -3,  1,      1, -1, -1,  3,
    # 	    -3, -1, -1,  1,     -1, -3, -1,  1,     -1, -1, -3,  1,     -1, -1, -1,  3,
    # 	     3,  1,  1, -1,      1,  3,  1, -1,      1,  1,  3, -1,      1,  1,  1, -3,
    # 	    -3,  1,  1, -1,     -1,  3,  1, -1,     -1,  1,  3, -1,     -1,  1,  1, -3,
    # 	     3, -1,  1, -1,      1, -3,  1, -1,      1, -1,  3, -1,      1, -1,  1, -3,
    # 	    -3, -1,  1, -1,     -1, -3,  1, -1,     -1, -1,  3, -1,     -1, -1,  1, -3,
    # 	     3,  1, -1, -1,      1,  3, -1, -1,      1,  1, -3, -1,      1,  1, -1, -3,
    # 	    -3,  1, -1, -1,     -1,  3, -1, -1,     -1,  1, -3, -1,     -1,  1, -1, -3,
    # 	     3, -1, -1, -1,      1, -3, -1, -1,      1, -1, -3, -1,      1, -1, -1, -3,
    # 	    -3, -1, -1, -1,     -1, -3, -1, -1,     -1, -1, -3, -1,     -1, -1, -1, -3,
    # 	}
# }
#  OpenSimplexNoiseTest.java
# /*
#  * OpenSimplex Noise sample class.
#  */
#
# import java.awt.image.BufferedImage
# import javax.imageio.ImageIO
# import java.io.*
#
# public class OpenSimplexNoiseTest
# {
# 	private static final int WIDTH = 512
# 	private static final int HEIGHT = 512
# 	private static final FEATURE_SIZE = 24
#
# 	public static void main(String[] args)
# 		throws IOException {
#
# 		OpenSimplexNoise noise = new OpenSimplexNoise()
# 		BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB)
# 		for (int y = 0; y < HEIGHT; y++)
# 		{
# 			for (int x = 0; x < WIDTH; x++)
# 			{
# 				value = noise.eval(x / FEATURE_SIZE, y / FEATURE_SIZE, 0.0)
# 				int rgb = 0x010101 * (int)((value + 1) * 127.5)
# 				image.setRGB(x, y, rgb)
# 			}
# 		}
# 		ImageIO.write(image, "png", new File("noise.png"))
# 	}
# }
#  UNLICENSE
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
