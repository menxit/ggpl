from pyplasm import *
from larlib import *
import os
from Utilities import *


class Brecciolino:

    assets = []

    def __init__(self, assets):
        self.assets = assets

    def render(self):
        """
        Returns the brecciolino

        :return:
        """

        results = []
        script_dir = os.path.dirname(__file__)

        for asset in self.assets:
            file_path = os.path.join(script_dir, asset['file'])
            nodes, edges = Utilities().lines_to_graph(file_path)
            points = map(lambda (x, y): [x, y], nodes)
            print points
            result = MKPOL([points, [range(1, len(points))], None])
            results.append(result)

        return results

