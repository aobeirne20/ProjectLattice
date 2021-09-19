import math
import random
import numpy as np

import geometric_elements as ge

class LG1_LondonNormal:
    def __init__(self, xgs, ygs, map):
        self.render_list = []
        self.xgs = xgs
        self.ygs = ygs

    def generate(self):
        # Pick starting location
        starting_location = (random.randint(int(self.xgs/3), int(3*self.xgs/3*2)),
                             random.randint(int(self.ygs/3), int(3*self.ygs/3*2)))
        current_location = starting_location
        current_direction = np.random.choice([0, 45, 90, 180, 225, 270, 315])
        reverse_direction = 360 - current_direction

        moving = True
        while moving:

    def step(self):

    def branch(self):

    def intersect(self):
