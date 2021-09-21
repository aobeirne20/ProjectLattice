import math
import random as r
import numpy as np

import geometric_elements as ge
from LineGenerators import LG1_LondonNormalHelper as lnh
from LineGenerators import LG1_Config as config


class LG1_LondonNormal:
    def __init__(self, xs, ys, map):
        self.render_list = []
        self.map = map
        self.xs = xs
        self.ys = ys
        self.trend_direction = None
        self.termination_score = config.termination_score
        self.buffer = []

    # Top-level generate
    def generate(self):
        current = self.first_segment()
        self.continuing_segments(current)
        for thing in self.buffer:
            if thing[1] != '360':
                self.render_list.append(thing[1])
        #self.termination(current)
        return self.render_list

    def first_segment(self):
        # Placing and checking the origin point
        current, zone = self.origin()

        # Choosing and checking the first segment
        posdir, self.trend_direction = lnh.pick_start_dir(xs=self.xs, ys=self.ys, starting_location=current, zone=zone)
        next_posdir, next_segment, distance = lnh.create_straight(xs=self.xs, ys=self.ys, posdir=posdir, force_distance=None)
        while lnh.check_start_dir(next_posdir=next_posdir, next_segment=next_segment, map_network=self.map) is False:
            current, zone = self.origin()
            posdir, self.trend_direction = lnh.pick_start_dir(xs=self.xs, ys=self.ys, starting_location=current, zone=zone)
            next_posdir, next_segment, distance = lnh.create_straight(xs=self.xs, ys=self.ys, posdir=posdir, force_distance=None)

        # Add to list
        self.render_list.append(next_segment)
        return next_posdir

    def origin(self):
        current, zone = lnh.pick_start_loc(xs=self.xs, ys=self.ys)
        while lnh.check_start_loc(starting_location=current, map_network=self.map) is False:
            current, zone = lnh.pick_start_loc(xs=self.xs, ys=self.ys)
        return current, zone

    def continuing_segments(self, current_posdir):
        while self.termination_score > 0:
            curve, next_posdir, segment, next2_posdir = self.next_segment(current_posdir)
            if curve is None:
                self.buffer.append([current_posdir, '360', next_posdir])
            else:
                self.buffer.append([current_posdir, curve, next_posdir])
            self.buffer.append([next_posdir, segment, next2_posdir])


            current_posdir = next2_posdir

            self.termination_score -= 250
            checkr = self.check_next()
            if checkr is not None:
                current_posdir = checkr


    def check_next(self):
        # Check 1: Is the end of the most recent segment + curve radius outside the map:
        if lnh.is_inside_boundaries(xs=self.xs, ys=self.ys, buffer1=self.buffer[-2], buffer2=self.buffer[-1]) is not True:
            trash = self.buffer.pop()
            trash2 = self.buffer.pop()
            return trash2[0]





    def next_segment(self, current_posdir):
        next_posdir, curve = lnh.pick_next_curve(posdir=current_posdir, trend=self.trend_direction, force_change=None)
        next2_posdir, segment, distance = lnh.create_straight(xs=self.xs, ys=self.ys, posdir=next_posdir, force_distance=None)
        return curve, next_posdir, segment, next2_posdir

    def termination(self):
        pass












