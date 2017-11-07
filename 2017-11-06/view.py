from pyplasm import *
from lib.chiesa import *

VIEW(STRUCT([
    HEX("#2C522E")(CUBOID([100,100])),
    HEX(C1)(T(1)(50-10)(CUBOID([20,100]))),
    HEX(C1)(T(2)(50-10)(CUBOID([100, 20]))),
    T([1, 2])([50, 50])(chiesa(20, 20)),
    T([1, 2])([90, 50])(chiesa(10, 10)),
    T([1, 2])([10, 50])(chiesa(10, 8, 4))
]))

quit()
