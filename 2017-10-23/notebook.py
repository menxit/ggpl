from larlib import *

Leg = CUBOID([0.1, 0.1, 0.7])
Plane = CUBOID([1, 1, 0.2])
Table = STRUCT([Leg, T(1)(0.9)(Leg), T(2)(0.9)(Leg), T([1, 2])([0.9, 0.9])(Leg), T(3)(0.7)(Plane)])

ColoredTable = HEX("#8B4513")(Table)

VIEW(ColoredTable)
