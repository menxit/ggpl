from pyplasm import *
from lib.church import *

VIEW(STRUCT([
    HEX("#2C522E")(CUBOID([100,100])),
    HEX("#cecece")(T(1)(50-10)(CUBOID([20,100]))),
    HEX("#cecece")(T(2)(50-10)(CUBOID([100, 20]))),
    T([1, 2])([50, 50])(church(20, 8)),
    T([1, 2])([90, 50])(church(10, 8, 1.618)),
    T([1, 2])([10, 50])(church(10, 4, 2))
]))

quit()
