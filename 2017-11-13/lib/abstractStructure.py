from pyplasm import STRUCT, R
from arch import *


def abstractStructure(N, half=True):
    """
    Struttura astratta che restituisce N archi ruotati ciascuno di i*2*PI

    :param N:
    :param half:
    :return:
    """
    return STRUCT(map(lambda x: R([1, 3])(x * (2 * PI) / N)(arch(rr=20, w=2, half=half)), range(0, N)))
