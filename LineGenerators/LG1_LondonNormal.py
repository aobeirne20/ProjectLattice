import math
import random as r
import numpy as np

import geometric_elements as ge
import LG1_LondonNormalHelper as lnh


straight_unit_vectors = {0: (1, 0),
                        45: (math.sqrt(0.5), -1*math.sqrt(0.5)),
                        90: (0, -1),
                        135: (-1*math.sqrt(0.5), -1*math.sqrt(0.5)),
                        180: (-1, 0),
                        225: (-1*math.sqrt(0.5), math.sqrt(0.5)),
                        270: (0, 1),
                        315: (math.sqrt(0.5), math.sqrt(0.5)),
                        360: (1, 0)}
rd_to_curve_displacer = {315: 0, 45: 90, 135: 180, 225: 270}
ld_to_curve_displacer = {}
curve_displacement = {90: np.array(([1], [-1])), -90: np.array(([1], [1])), 45: np.array(([2], [-1])), -45: np.array(([2], [1]))}
curve_displacement_dx = {45: np.array(([1], [-2])), -45: np.array(([1], [2]))}
rotate_array_dict = {90: np.array(([0, 1], [-1, 0])), -90: np.array(([0, -1], [1, 0])),
                     45: np.array(([0, math.sqrt(0.5)], [-1*math.sqrt(0.5), 0])), -45: np.array(([0, -1*math.sqrt(0.5)], [math.sqrt(0.5), 0]))}
rotate_instructions = {0: [], 45: [45], 90: [90], 135: [90, 45], 180: [90, 90], 225: [90, 90, 45], 270: [90, 90, 90], 315: [90, 90, 90, 45]}


class LG1_LondonNormal:
    def __init__(self, xs, ys, map):
        self.render_list = []
        self.map = map
        self.xs = xs
        self.ys = ys

    def top_level_generate(self):
        current = self.first_segment()
        #current = self.continuing_segments(current)
        #self.termination(current)

    def first_segment(self):
        current = lnh.pick_start_loc(xs=self.xs, ys=self.ys)
        while lnh.check_start_loc(starting_location=current, map_network=self.map)

    def continuing_segments(self):
        # Iterative method

    def termination(self):











