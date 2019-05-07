from Matrix import IdentityMatrix


def Translation(x, y, z):
    m = IdentityMatrix(4)
    m[0][3] = x
    m[1][3] = y
    m[2][3] = z
    return m
