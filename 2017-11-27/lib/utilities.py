import csv
import math

def linesToGraph(filePath):
    """
    Questa funzione prende in input un file di linee e lo strasforma in un grafo

    :param file:
    :return:
    """
    with open(filePath, "rb") as file:

        reader = csv.reader(file, delimiter=",")

        keys = {}
        nodi = []
        archi = []

        i = 0

        for row in reader:
            """
            Effettuo l'approssimazione dei punti delle linee
            """
            row0 = math.floor(float(row[0]) / 10) * 10
            row1 = math.floor(float(row[1]) / 10) * 10
            row2 = math.floor(float(row[2]) / 10) * 10
            row3 = math.floor(float(row[3]) / 10) * 10

            if not (row0, row1) in keys.keys():
                keys[(row0, row1)] = i
                nodi.append((row0, row1))
                i = i + 1

            if not (row2, row3) in keys.keys():
                keys[(row2, row3)] = i
                nodi.append((row2, row3))
                i = i + 1

            archi.append((keys[(row0, row1)], (keys[(row2, row3)])))

    return (nodi, archi)
