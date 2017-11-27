import os
from pyplasm import STRUCT, OFFSET, POLYLINE, MULTEXTRUDE
import math
import csv

scriptDir = os.path.dirname(__file__)

def planimetria(spessore = 3, h_laterale = 50, h_centrale = 100):
    """
    Planimetria della villa
    :param spessore:
    :param h_laterale:
    :param h_centrale:
    :return:
    """
    muri_laterali = []
    muri_centrale = []
    with open(os.path.join(scriptDir, "../assets/centrale.lines"), "rb") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            row0 = math.floor(float(row[0])/10)*10
            row1 = math.floor(float(row[1])/10)*10
            row2 = math.floor(float(row[2])/10)*10
            row3 = math.floor(float(row[3])/10)*10
            muri_laterali.append(OFFSET([spessore, spessore])(POLYLINE([[row0, row1], [row2, row3]])))

    with open(os.path.join(scriptDir, "../assets/laterale.lines"), "rb") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            row0 = math.floor(float(row[0])/10)*10
            row1 = math.floor(float(row[1])/10)*10
            row2 = math.floor(float(row[2])/10)*10
            row3 = math.floor(float(row[3])/10)*10
            muri_centrale.append(OFFSET([spessore, spessore])(POLYLINE([[row0, row1], [row2, row3]])))

    muri_laterali = STRUCT(muri_laterali)
    muri_laterali = (muri_laterali)

    muri_centrale = STRUCT(muri_centrale)
    muri_centrale = (muri_centrale)

    return STRUCT([MULTEXTRUDE(muri_laterali)(h_laterale), MULTEXTRUDE(muri_centrale)(h_centrale)])
