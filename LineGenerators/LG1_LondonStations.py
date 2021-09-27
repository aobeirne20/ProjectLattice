import math
import random as r
import numpy as np
import shapely

import style_data as sd
import geometric_elements as ge
from LineGenerators import LG1_LondonNormalHelper as lnh
from LineGenerators import LG1_Config as config
from MiscRenderers import RM3_LondonTextPreparer
from PIL import Image, ImageDraw, ImageFont
import PIL

straight_unit_vectors = {0: (1, 0), 45: (math.sqrt(0.5), -1 * math.sqrt(0.5)), 90: (0, -1), 135: (-1 * math.sqrt(0.5), -1 * math.sqrt(0.5)),
                         180: (-1, 0), 225: (-1 * math.sqrt(0.5), math.sqrt(0.5)), 270: (0, 1), 315: (math.sqrt(0.5), math.sqrt(0.5)), 360: (1, 0)}
anchor_dict = {0: 'lm', 45: 'ld', 90: 'md', 135: 'rd', 180: 'rm', 225: 'ra', 270: 'ma', 315: 'la', 999: 'lm'}


class LG1_LondonStations:
    def __init__(self, xs, ys, map, text_giver):
        self.map = map
        self.xs = xs
        self.ys = ys
        self.locus_list = self.map.locus_list
        self.text_giver = text_giver
        self.current_stations = []

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

            if length / 2 <= config.station_distance:
                continue

            while True:
                name = self.text_giver.give_name(line.style['name_type'])
                if orientation == 90 or orientation == 270:
                    chosen_name = name[0]
                else:
                    chosen_name = name[-1]
                if pattern is None:
                    pattern = r.randint(config.station_distance, int(length / 2))

                current_distance += pattern
                if current_distance > length:
                    break

                vector_along = (
                    current_distance * lnh.straight_unit_vectors[orientation][0],
                    current_distance * lnh.straight_unit_vectors[orientation][1])

                tick_orientation = orientation + 90
                if tick_orientation >= 360:
                    tick_orientation -= 360

                second_orientation = tick_orientation + 180
                if second_orientation >= 360:
                    second_orientation -= 360

                current_station1 = {'location': (loc1[0] + vector_along[0], loc1[1] + vector_along[1]), 'name': 'Single',
                                    'orientation': tick_orientation, 'text': chosen_name}
                current_station2 = {'location': (loc1[0] + vector_along[0], loc1[1] + vector_along[1]), 'name': 'Single',
                                    'orientation': second_orientation, 'text': chosen_name}

                a = lnh.PositionAndDirection(x=current_station1['location'][0], y=current_station1['location'][1], dirc=0)
                b = lnh.PositionAndDirection(x=current_station2['location'][0], y=current_station2['location'][1], dirc=0)

                tick_vector_a = (
                    19 * lnh.straight_unit_vectors[tick_orientation][0],
                    19 * lnh.straight_unit_vectors[tick_orientation][1])

                tick_vector_b = (
                    19 * lnh.straight_unit_vectors[second_orientation][0],
                    19 * lnh.straight_unit_vectors[second_orientation][1])

                a.x = a.x + tick_vector_a[0]
                a.y = a.y + tick_vector_a[1]

                b.x = b.x + tick_vector_b[0]
                b.y = b.y + tick_vector_b[1]

                dist_report1 = self.map.node_check_exclusion(a, line.name)
                dist_report2 = self.map.node_check_exclusion(b, line.name)

                if dist_report1['distance'] < 40 * sd.StyleDatabase.t_scale or dist_report2['distance'] < 40 * sd.StyleDatabase.t_scale:
                    continue

                if dist_report1['distance'] > dist_report2['distance']:
                    current_station1['text_location'] = (a.x, a.y)
                    self.current_stations.append(current_station1)
                else:
                    current_station2['text_location'] = (b.x, b.y)
                    self.current_stations.append(current_station2)

                if np.random.choice([True, False], p=[0.4, 0.6]):
                    pattern *= r.uniform(0.5, 1.5)
                    if pattern < config.station_distance:
                        pattern = None

        return self.current_stations

    def location_searcher(self, locus, font, draw):
        name = self.text_giver.give_name(locus['type'])
        for distance in [28, 36, 40]:
            for direction in [0, 45, 135, 180, 225, 315]:
                first_time = True
                while True:
                    if first_time is True:
                        if len(name) > 1:
                            if direction == 90 or direction == 270:
                                name_version = -2
                            else:
                                name_version = -1
                        else:
                            name_version = -1
                        first_time = False

                    xy = (locus['location'][0] + straight_unit_vectors[direction][0] * distance,
                          locus['location'][1] + straight_unit_vectors[direction][1] * distance)

                    bbox = draw.multiline_textbbox(xy, name[name_version], font=font, anchor=anchor_dict[direction])

                    seg1 = ge.Segment(loc1=(bbox[0], bbox[1]), loc2=(bbox[2], bbox[1]), dis=1, orientation=0)
                    seg2 = ge.Segment(loc1=(bbox[2], bbox[1]), loc2=(bbox[2], bbox[3]), dis=1, orientation=270)
                    seg3 = ge.Segment(loc1=(bbox[2], bbox[3]), loc2=(bbox[0], bbox[3]), dis=1, orientation=180)
                    seg4 = ge.Segment(loc1=(bbox[0], bbox[3]), loc2=(bbox[0], bbox[1]), dis=1, orientation=90)

                    check1 = self.map.seg_crossing_check(seg1)
                    check2 = self.map.seg_crossing_check(seg2)
                    check3 = self.map.seg_crossing_check(seg3)
                    check4 = self.map.seg_crossing_check(seg4)

                    if check1 and check2 and check3 and check4:
                        current_station = {'location': xy, 'name': 'Interchange', 'orientation': direction, 'text': name[name_version]}
                        return current_station
                    else:
                        if abs(name_version) < len(name):
                            name_version -= 1
                        else:
                            break
        return None













