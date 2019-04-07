# Specific maths functions for raytrace

EPSILON = 0.00001


def equals(a, b):
    if abs(a-b) < EPSILON:
        return True
    else:
        return False
