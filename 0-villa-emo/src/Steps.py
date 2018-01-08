from pyplasm import *


class Steps:

    def __init__(self, steps, width, height, depth):
        self.width = float(width)
        self.height = float(height)
        self.depth = float(depth)
        self.steps = steps

    def render(self):
        steps = map(self._get_step, range(0, self.steps))
        return STRUCT(steps)

    def _get_step(self, index):
        s_height = self.height/self.steps
        s_depth = self.depth/self.steps
        return T(2)(s_depth*index)(CUBOID([self.width, s_depth, (index+1)*s_height]))
