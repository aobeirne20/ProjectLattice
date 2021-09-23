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

        # FIRST PRIME BRANCH
        path = [PathElement(flip_posdir, 'origin', origin_posdir)]
        term_score = t_score(self.xs, self.ys)
        child_error, path = self.r_gen_package(path=path, trend=trend, termination_score=term_score, instruction=Instruction('first_seg'))
        if child_error is None:
            path_buffer += path
        else:
            return self.outer_generate()

        # SECOND PRIME BRANCH
        path = [PathElement(origin_posdir, 'origin', flip_posdir)]
        term_score = t_score(self.xs, self.ys)
        child_error, path = self.r_gen_package(path=path, trend=flip_trend, termination_score=term_score, instruction=Instruction('first_seg'))
        if child_error is None:
            path_buffer += path
        else:
            return self.outer_generate()

        self.process_branches(path_buffer)
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

    def r_gen_package(self, path, trend, instruction, termination_score):
        # PACKAGE GENERATION
        path_addenum, change, next_distance = make_package(path, trend, self.xs, self.ys, instruction)

        # SANDWICH GENERATOR
        is_gross_sandwich = lnh.is_wrong_sandwich(path_addenum[1].part, self.map)
        if is_gross_sandwich:
            child_error, path = self.r_gen_package(path + path_addenum, trend, None, termination_score - next_distance)



        # LINE TERMINATION
        if lnh.is_inside_boundaries(xs=self.xs, ys=self.ys, postdir=path_addenum[1].next_posdir) is False:
            return None, path
        elif termination_score - next_distance < 0:
            return None, path

        # CONTINUING GENERATION
        child_error, path = self.r_gen_package(path + path_addenum, trend, None, termination_score-next_distance)
        if child_error is None:
            return None, path
        else:
            # handle child error
            pass

    def r_terminus(self, path, trend):
        return None, path

    def process_branches(self, path_list):
        for part in path_list:
            #print(part.part)
            pass







def make_package(path, trend, xs, ys, instruction):
    if instruction is None:
        force_change = None
        force_distance = None
        mod_distance_f = None
    else:
        force_change, force_distance, mod_distance_f = instruction.execute()

    current_posdir = path[-1].next_posdir
    middle_posdir, next_curve, change = lnh.pick_next_curve(current_posdir, trend, force_change=force_change)
    end_posdir, next_segment, next_distance = lnh.create_straight(xs, ys, middle_posdir, force_distance=force_distance, mod_distance_f=mod_distance_f)

    if next_curve is None:
        next_curve = 'straight'
    path_addenum = [PathElement(current_posdir, next_curve, middle_posdir), PathElement(middle_posdir, next_segment, end_posdir)]
    return path_addenum, change, next_distance






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


def t_score(xs, ys):
    t_s = math.sqrt((xs/2) ** 2 + (ys/2) ** 2) * r.uniform(config.termination_score_min_max[0], config.termination_score_min_max[1])
    return t_s


class ChildErrorPackage:
    def __init__(self):
        pass


class PathElement:
    def __init__(self, previous_posdir, part, next_posdir):
        self.previous_posdir = previous_posdir
        self.part = part
        self.next_posdir = next_posdir


class Instruction:
    def __init__(self, command):
        self.command = command

    def execute(self):
        if self.command == 'first_seg':
            return 0, None, 0.5
        else:
            print(f"Command not registered")



























