from Matrix import IdentityMatrix
from math import sin, cos

def Translation(x, y, z):
    m = IdentityMatrix(4)
    m[0][3] = x
    m[1][3] = y
    m[2][3] = z
    return m


def Scaling(x, y, z):
    m = IdentityMatrix(4)
    m[0][0] = x
    m[1][1] = y
    m[2][2] = z
    return m


def Rotation_x(rads):
    m = IdentityMatrix(4)
    m[1][1] = cos(rads)
    m[1][2] = -sin(rads)
    m[2][1] = sin(rads)
    m[2][2] = cos(rads)
    return m


def Rotation_y(rads):
    m = IdentityMatrix(4)
    m[0][0] = cos(rads)
    m[0][2] = sin(rads)
    m[2][0] = -sin(rads)
    m[2][2] = cos(rads)
    return m


def Rotation_z(rads):
    m = IdentityMatrix(4)
    m[0][0] = cos(rads)
    m[0][1] = -sin(rads)
    m[1][0] = sin(rads)
    m[1][1] = cos(rads)
    return m


def Shearing(xy, xz, yx, yz, zx, zy):
    m = IdentityMatrix(4)
    m[0][1] = xy
    m[0][2] = xz
    m[1][0] = yx
    m[1][2] = yz
    m[2][0] = zx
    m[2][1] = zy
    return m
