import csv
from pyplasm import *


class Utilities:

    @staticmethod
    def lines_to_graph(file_path):
        """
        Questa funzione prende in input un file di linee e lo strasforma in un grafo

        :param file:
        :return:
        """
        with open(file_path, "rb") as file:

            reader = csv.reader(file, delimiter=",")

            keys = {}
            nodes = []
            edges = []

            i = 0

            for row in reader:
                row0 = round(float(row[0]) / 10) * 10
                row1 = round(float(row[1]) / 10) * 10
                row2 = round(float(row[2]) / 10) * 10
                row3 = round(float(row[3]) / 10) * 10

                if not (row0, row1) in keys.keys():
                    keys[(row0, row1)] = i
                    nodes.append((row0, row1))
                    i = i + 1

                if not (row2, row3) in keys.keys():
                    keys[(row2, row3)] = i
                    nodes.append((row2, row3))
                    i = i + 1

                edges.append((keys[(row0, row1)], (keys[(row2, row3)])))

        print nodes, edges
        return nodes, edges

