import random
import math
from pyplasm import STRUCT, PI, T, HEX, R


def randomColor():
    """
    Return a random HEX color

    :return:
    """
    return "#%06x" % random.randint(0, 0xFFFFFF)


def arrangedCircularly(o, r, n):
    """
    Dispone l'oggetto o, in un raggio immaginario r, n oggetti.

    :param o:
    :param r:
    :param n:
    :return:
    """
    return STRUCT(map(lambda i: T([1, 2])([
        r*math.cos((2 * PI / n) * i),
        r*math.sin((2 * PI / n) * i)
    ])(R([1, 2])((2 * PI / n) * i)(HEX(randomColor())(o))), range(0, n)))
