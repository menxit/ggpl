from pyplasm import *
from larlib import *
import os
from Utilities import *

class Planimetry:

    assets = []

    def __init__(self, assets):
        self.assets = assets

    def render(self):
        """
        Returns the planimetry

        :return:
        """

        results = []
        script_dir = os.path.dirname(__file__)

        for asset in self.assets:
            file_path = os.path.join(script_dir, asset['file'])
            nodes, edges = Utilities().lines_to_graph(file_path)
            result = MULTEXTRUDE(OFFSET([2, 2])(STRUCT(MKPOLS((nodes, edges)))))(asset['height'])
            results.append(result)

        return T([1, 2, 3])([0, -247, 0])(STRUCT(results))

