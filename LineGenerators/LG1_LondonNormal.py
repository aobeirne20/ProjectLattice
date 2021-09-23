import math
import random as r
import numpy as np

import geometric_elements as ge
from LineGenerators import LG1_LondonNormalHelper as lnh
from LineGenerators import LG1_Config as config


class LG1_LondonNormal:
    def __init__(self, xs, ys, map):
        self.map = map
        self.xs = xs
        self.ys = ys

    def outer_generate(self):
        # ORIGIN
        path_buffer = []
        origin_posdir, trend, flip_posdir, flip_trend = self.gen_origin()
        print(trend)

        # FIRST PRIME BRANCH
        path = [PathElement(flip_posdir, 'origin', origin_posdir)]
        child_error, path = self.r_gen_package(path=path, trend=trend)
        if child_error is None:
            path_buffer += path
        else:
            return self.outer_generate()

        # SECOND PRIME BRANCH
        path = [PathElement(origin_posdir, 'origin', flip_posdir)]
        child_error, path = self.r_gen_package(path=path, trend=flip_trend)
        if child_error is None:
            path_buffer += path
        else:
            return self.outer_generate()

        render_list = unload_buffer(path_buffer)
        return render_list

    def gen_origin(self):
        # Calculate chance to start on an interchange
        potential_start_interchanges = lnh.potential_start_stations(xs=self.xs, ys=self.ys, map_network=self.map)
        chance = math.sqrt(len(potential_start_interchanges) * 0.5) / 8
        p_chance_to_start_on_int = [chance, 1 - chance]

        # CHOICE: True, start on interchange; False, start on random location
        if np.random.choice([True, False], p=p_chance_to_start_on_int) and potential_start_interchanges:
            origin_posdir = np.random.choice(potential_start_interchanges)
        else:
            origin_posdir = lnh.pick_start_loc(xs=self.xs, ys=self.ys)
            while lnh.check_start_loc(starting_location=origin_posdir, map_network=self.map) is False:
                origin_posdir = lnh.pick_start_loc(xs=self.xs, ys=self.ys)

        # Get origin direction and trend
        origin_posdir, trend = lnh.pick_start_dir(origin_posdir)

        # Prepare flip
        flip_posdir = lnh.PositionAndDirection(origin_posdir.x, origin_posdir.y, flip_angle(origin_posdir.dirc))
        flip_trend = flip_angle(trend)

        # Return to function
        return origin_posdir, trend, flip_posdir, flip_trend

    def r_gen_package(self, path, trend):
        # PACKAGE GENERATION
        current_posdir = path[-1].next_posdir
        middle_posdir, next_curve, change = lnh.pick_next_curve(current_posdir, trend, force_change=None)
        end_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, middle_posdir, force_distance=None)

        # LINE TERMINATION
        if lnh.is_inside_boundaries(xs=self.xs, ys=self.ys, postdir=end_posdir) is False:
            return None, path

        else:
            if next_curve is None:
                next_curve = 'straight'
            path_addenum = [PathElement(current_posdir, next_curve, middle_posdir), PathElement(middle_posdir, next_segment, end_posdir)]
            child_error, path = self.r_gen_package(path + path_addenum, trend)
            if child_error is None:
                return None, path
            else:
                # handle child error
                pass







def flip_angle(angle):
    new_angle = angle + 180
    if new_angle >= 360:
        new_angle -= 360
    return new_angle

def unload_buffer(path_buffer):
    render_list = []
    for path_element in path_buffer:
        if isinstance(path_element.part, str):
            pass
        else:
            render_list.append(path_element.part)
    return render_list




class ChildErrorPackage:
    def __init__(self):
        pass


class PathElement:
    def __init__(self, previous_posdir, part, next_posdir):
        self.previous_posdir = previous_posdir
        self.part = part
        self.next_posdir = next_posdir






























