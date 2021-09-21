import numpy as np
import random as r

import LG1_Config as config

start_pair = {(1, 1): [90, 135, 180], (-1, 1): [0, 45, 90], (-1, -1): [0, 315, 270], (1, -1): [180, 225, 270]}
slz = [[1/20, 1/3], [2/3, 19/20]]


class PositionAndDirection:
    def __init__(self, x, y, dirc):
        self.x = x
        self.y = y
        self.dirc = dirc

    def orientation_change(self, change):
        direction = self.dirc + change
        if direction >= 360:
            direction -= 360
        elif direction < 0:
            direction += 360
        self.dirc = direction
        return self.dirc


def pick_start_loc(xs, ys):
    # Maybe expand this section later to have 6 zones instead of 4 quadrants
    x_list = []
    y_list = []
    for zone in slz:
        x_list.append(r.randint(int(zone[0] * xs), int(zone[1] * xs)))
        y_list.append(r.randint(int(zone[0] * ys), int(zone[1] * ys)))
    starting_location = PositionAndDirection(np.random.choice(x_list), np.random.choice(y_list), None)
    return starting_location


def check_start_loc(starting_location, map_network):
    if map_network.node_check(starting_location)["distance"] < config.starting_exclusion_scale:
        return False
    else:
        return True













