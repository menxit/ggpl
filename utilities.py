from larlib import T


def XYZ(coordinates):
    return T([1, 2, 3])([coordinates[0] or 0, coordinates[1] or 0, coordinates[2] or 0])
