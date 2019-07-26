import Matrix
from math import sin, cos


def Translation(x, y, z):
    m = Matrix.IdentityMatrix(4)
    m[0][3] = x
    m[1][3] = y
    m[2][3] = z
    return m


def Scaling(x, y, z):
    m = Matrix.IdentityMatrix(4)
    m[0][0] = x
    m[1][1] = y
    m[2][2] = z
    return m


def Rotation_x(rads):
    m = Matrix.IdentityMatrix(4)
    m[1][1] = cos(rads)
    m[1][2] = -sin(rads)
    m[2][1] = sin(rads)
    m[2][2] = cos(rads)
    return m


def Rotation_y(rads):
    m = Matrix.IdentityMatrix(4)
    m[0][0] = cos(rads)
    m[0][2] = sin(rads)
    m[2][0] = -sin(rads)
    m[2][2] = cos(rads)
    return m


def Rotation_z(rads):
    m = Matrix.IdentityMatrix(4)
    m[0][0] = cos(rads)
    m[0][1] = -sin(rads)
    m[1][0] = sin(rads)
    m[1][1] = cos(rads)
    return m


def Shearing(xy, xz, yx, yz, zx, zy):
    m = Matrix.IdentityMatrix(4)
    m[0][1] = xy
    m[0][2] = xz
    m[1][0] = yx
    m[1][2] = yz
    m[2][0] = zx
    m[2][1] = zy
    return m


def ViewTransform(p_from, p_to, v_up):
    forward = (p_to - p_from).normalize()
    left = forward.cross(v_up.normalize())
    true_up = left.cross(forward)
    orientation = Matrix.Matrix([[left.x, left.y, left.z, 0],
                                 [true_up.x, true_up.y, true_up.z, 0],
                                 [-forward.x, -forward.y, -forward.z, 0],
                                 [0, 0, 0, 1]])
    vt = orientation * Translation(-p_from.x, -p_from.y, -p_from.z)
    return vt
