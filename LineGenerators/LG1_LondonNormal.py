import math
import random as r
import numpy as np

import geometric_elements as ge

# Starting locations: To, and then from
slz = [1/3, 2/3]

class LG1_LondonNormal:
    def __init__(self, xs, ys, map):
        self.render_list = []
        self.map = []
        self.xs = xs
        self.ys = ys

    def generate(self):
        pass

    def generate_main(self):
        # Pick starting location, and line trend
        starting_location = (np.random.choice([r.randint(0, int(slz[0]) * self.xs),
                                               r.randint(int(slz[1]) * self.xs, self.xs)]),
                             np.random.choice([r.randint(0, int(slz[0]) * self.ys),
                                               r.randint(int(slz[1]) * self.ys, self.ys)]))




        current_location = starting_location
        trend_direction = np.random.choice([0, 45, 90, 180, 225, 270, 315])
        current_direction = np.random.choice([0, 45, 90, 180, 225, 270, 315])

        moving = True

    def generate_branch(self):
        pass
