import math
import random as r
import numpy as np

import geometric_elements as ge
from LineGenerators import LG1_LondonNormalHelper as lnh
from LineGenerators import LG1_Config as config


class LG1_LondonStations:
    def __init__(self, xs, ys, map):
        self.map = map
        self.xs = xs
        self.ys = ys

    def generate_stations(self, line):
        temp_segment_list = []
        for thing in line.render_list:
            if isinstance(thing, ge.Segment):
                temp_segment_list.append(thing)

        current_stations = []
        for thing in temp_segment_list:


            loc1 = thing.loc1

            length = thing.distance
            orientation = thing.orientation

            current_distance = 0
            pattern = None


            if length/2 <= config.station_distance:
                continue

            while True:
                if pattern is None:
                    pattern = r.randint(config.station_distance, int(length / 2))

                current_distance += pattern
                if current_distance > length:
                    break

                vector_along = (
                    current_distance * lnh.straight_unit_vectors[orientation][0],
                    current_distance * lnh.straight_unit_vectors[orientation][1])

                tick_orientation = orientation+90
                if tick_orientation >= 360:
                    tick_orientation -= 360
                current_stations.append({'location': (loc1[0] + vector_along[0], loc1[1] + vector_along[1]), 'name': 'Single', 'orientation': tick_orientation})

                if np.random.choice([True, False], p=[0.4, 0.6]):
                    pattern *= r.uniform(0.5, 1.5)
                    if pattern < config.station_distance:
                        pattern = None

            for potential_stations in current_stations:
                pass

        return current_stations







