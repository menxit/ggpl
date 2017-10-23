from larlib import \
    CUBOID, \
    STRUCT, \
    T, \
    HEX


def table():
    """ table

    A table created with PyPlasm.

    :return:
    """
    leg = CUBOID([0.1, 0.1, 0.7])
    plane = CUBOID([1, 1, 0.2])

    return HEX("#8B4513")(STRUCT([leg, T(1)(0.9)(leg), T(2)(0.9)(leg), T([1, 2])([0.9, 0.9])(leg), T(3)(0.7)(plane)]))
