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


class LG1_LondonInterchanges:
    def __init__(self, xs, ys, map, text_giver):
        self.map = map
        self.xs = xs
        self.ys = ys
        self.locus_list = self.map.locus_list
        self.text_giver = text_giver
        self.current_stations = []

    def generate_stations(self):
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img_slice)
        font = ImageFont.truetype("ITC - JohnstonITCPro-Medium.otf", 25*sd.StyleDatabase.t_scale)
        for locus in self.map.locus_list:
            print(f"Searching for {locus}")
            posed_text = self.location_searcher(locus, font, draw)
            if posed_text is not None:
                self.current_stations.append(posed_text)
                print(posed_text)
            else:
                print("Failed")

        return self.current_stations

    def location_searcher(self, locus, font, draw):
        name = self.text_giver.give_name(locus['type'])
        first_time = True

        for distance in [20, 25, 30]:
            for direction in [0, 45, 135, 180, 225, 315]:

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

                    print(direction)
                    print(anchor_dict[direction])
                    bbox = draw.multiline_textbbox(xy, name[name_version], font=font, anchor=anchor_dict[direction])
                    print(bbox)


                    seg1 = ge.Segment(loc1=(bbox[0], bbox[1]), loc2=(bbox[2], bbox[1]), dis=bbox[2]-bbox[1], orientation=0)
                    seg2 = ge.Segment(loc1=(bbox[2], bbox[1]), loc2=(bbox[2], bbox[3]), dis=bbox[3]-bbox[1], orientation=270)
                    seg3 = ge.Segment(loc1=(bbox[2], bbox[3]), loc2=(bbox[0], bbox[3]), dis=bbox[0]-bbox[2], orientation=180)
                    seg4 = ge.Segment(loc1=(bbox[0], bbox[3]), loc2=(bbox[0], bbox[1]), dis=bbox[3]-bbox[1], orientation=90)

                    check1 = self.map.seg_crossing_check(seg1)
                    check2 = self.map.seg_crossing_check(seg2)
                    check3 = self.map.seg_crossing_check(seg3)
                    check4 = self.map.seg_crossing_check(seg4)

                    print(check1)
                    print(check2)
                    print(check3)
                    print(check4)

                    if bool(check1) and bool(check2) and bool(check3) and bool(check4):
                        current_station = {'text_location': xy, 'name': 'Interchange', 'orientation': direction, 'text': name[name_version]}
                        self.map.text_bbox_list.append((seg1, seg2, seg3, seg4))
                        return current_station
                    else:
                        if abs(name_version) < len(name):
                            name_version -= 1
                        else:
                            break
        return None
