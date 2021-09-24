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
        station_buffer = []
        origin_posdir, trend, flip_posdir, flip_trend = self.gen_origin()

        # FIRST PRIME BRANCH
        path = [PathElement(flip_posdir, 'origin', origin_posdir)]
        term_score = t_score(self.xs, self.ys)
        child_error, path, stations = self.r_gen_package(path=path, stations=[], trend=trend, termination_score=term_score, instruction=Instruction('first_seg'))
        if child_error is None:
            path_buffer += path
            station_buffer += stations
        else:
            return self.outer_generate()

        # SECOND PRIME BRANCH
        path = [PathElement(origin_posdir, 'origin', flip_posdir)]
        term_score = t_score(self.xs, self.ys)
        child_error, path, stations = self.r_gen_package(path=path, stations=[], trend=flip_trend, termination_score=term_score, instruction=Instruction('first_seg'))
        if child_error is None:
            path_buffer += path
            station_buffer += stations
        else:
            return self.outer_generate()

        self.process_branches(path_buffer)
        render_list, stations = unload_buffer(path_buffer, station_buffer)
        return render_list, stations

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

    def r_gen_package(self, path, stations, trend, instruction, termination_score):
        attempt_score = 100
        error_package = None
        sandwich = False
        while attempt_score > 0:
            # PACKAGE GENERATION
            path_addenum, change, next_distance = make_package(path, trend, self.xs, self.ys, instruction)

            # LINE TERMINATION
            if lnh.is_inside_boundaries(xs=self.xs, ys=self.ys, postdir=path_addenum[1].next_posdir) is False:
                return None, path, stations
            elif termination_score - next_distance < 0:
                return None, path, stations

            # SANDWICH ERROR / GENERATOR
            wrong_sandwich = lnh.wrong_sandwich(path_addenum[1].part, self.map)
            if wrong_sandwich:
                # Make a sandwich
                correct_sandwich = np.random.choice([True, False], p=[1, 0])
                # if wrong_sandwich['object'] != "LondonRiver" and correct_sandwich and change is not None:
                #     path = self.sandwich_maker(path=path, ws=wrong_sandwich, package=path_addenum, next_distance=next_distance)
                #     sandwich = True
                # else:
                error_package = ChildErrorPackage("PARALLEL_SEGMENT_ERROR")
                attempt_score -= 20
                continue

            # INTERCHANGE ERROR / GENERATION
            intr_lists = self.interchange_generation(path_addenum, change)
            finalized_interchanges = self.interchange_placement(intr_lists)
            checked_interchanges = []
            overall_valid = True
            for intr in finalized_interchanges:
                valid, do_place = lnh.check_for_interchange_dis(intr['location'], self.map)
                if valid is False:
                    overall_valid = False
                if do_place is True:

                    checked_interchanges.append(intr)
            if overall_valid is False:
                error_package = ChildErrorPackage("INTERCHANGE_CLOSENESS_ERROR")
                attempt_score -= 50
                continue
            stations += checked_interchanges


            # CONTINUING GENERATION
            if change is None:
                path = self.modify_last_segment(path=path, next_distance=next_distance)
                child_error, path, stations = self.r_gen_package(path, stations=stations, trend=trend,instruction=None, termination_score=termination_score - next_distance)
            else:
                child_error, path, stations = self.r_gen_package(path + path_addenum, stations=stations, trend=trend, instruction=None, termination_score=termination_score - next_distance)

            # RETURNING NON-ERROR PATH
            if child_error is None:
                return None, path, stations
            else:
                attempt_score = 100

        return error_package, path, stations

    def modify_last_segment(self, path, next_distance):
        old = path.pop()
        if old.part == 'origin':
            old_distance = 0
            old_posdir = old.next_posdir
        else:
            old_distance = old.part.distance
            old_posdir = old.previous_posdir
        new_distance = old_distance + next_distance
        end_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, old_posdir,
                                                            force_distance=new_distance, mod_distance_f=None)
        path.append(PathElement(old_posdir, next_segment, end_posdir))
        return path





    def interchange_generation(self, path_addenum, change):
        straight_on_straight = []
        straight_on_curve = []
        curve_on_straight = []
        curve_on_curve = []
        if change is None:
            interchange_list = lnh.check_for_interchange_new_straight(path_addenum[1].part, self.map)
            for intc in interchange_list:
                if intc['object'] == 'LondonRiver':
                    pass
                elif intc['geometry'] == 'Segment':
                    straight_on_straight.append(intc)
                else:
                    straight_on_curve.append(intc)
        else:
            interchange_list = lnh.check_for_interchange_new_curve(path_addenum[0].part, self.map)
            for intc in interchange_list:
                if intc['object'] == 'LondonRiver':
                    pass
                elif intc['geometry'] == 'Segment':
                    curve_on_straight.append(intc)
                else:
                    curve_on_curve.append(intc)
            interchange_list = lnh.check_for_interchange_new_straight(path_addenum[1].part, self.map)
            for intc in interchange_list:
                if intc['object'] == 'LondonRiver':
                    pass
                elif intc['geometry'] == 'Segment':
                    straight_on_straight.append(intc)
                else:
                    straight_on_curve.append(intc)
        return [straight_on_straight, straight_on_curve, curve_on_straight, curve_on_curve]

    def interchange_placement(self, intr_lists):
        finalized_intrs = []
        for intr in intr_lists[0]:
            if np.random.choice([True, False], p=config.P_seg_onto_seg):
                finalized_intrs.append({'location': intr['location'], 'name': 'Interchange'})
        for intr in intr_lists[1]:
            if np.random.choice([True, False], p=config.P_seg_onto_curve):
                finalized_intrs.append({'location': intr['location'], 'name': 'Interchange'})
        for intr in intr_lists[2]:
            if np.random.choice([True, False], p=config.P_curve_onto_seg):
                finalized_intrs.append({'location': intr['location'], 'name': 'Interchange'})
        for intr in intr_lists[3]:
            if np.random.choice([True, False], p=config.P_curve_onto_curve):
                finalized_intrs.append({'location': intr['location'], 'name': 'Interchange'})
        return finalized_intrs



    def r_terminus(self, path, trend):
        return None, path

    def process_branches(self, path_list):
        for part in path_list:
            #print(part.part)
            pass

    def sandwich_maker(self, path, ws, package, next_distance):
        # Find the distance along the previous path to change (+ longer, - shorter)




        distance_to_fix = config.sandwich_distance - ws['distance']

        print(f"Making sandwich with {ws['object']}")

        if positive_or_negative(from_seg=package[1].part, to_seg=ws['object']):
            distance_to_fix *= -1


        next_distance += distance_to_fix

        path = self.modify_last_segment(path, next_distance)

        return path



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



def positive_or_negative(from_seg, to_seg):
    if from_seg.orientation == 180 or from_seg.orientation == 0:
        if from_seg.loc1[1] > to_seg.loc1[1]:
            return -1
        else:
            return 1

    elif from_seg.orientation == 90 or from_seg.orientation == 270:
        if from_seg.loc1[1] > to_seg.loc1[1]:
            return -1
        else:
            return 1

    return 1




def flip_angle(angle):
    new_angle = angle + 180
    if new_angle >= 360:
        new_angle -= 360
    return new_angle


def unload_buffer(path_buffer, station_buffer):
    render_list = []
    for path_element in path_buffer:
        if isinstance(path_element.part, str):
            pass
        else:
            render_list.append(path_element.part)
    return render_list, station_buffer


def t_score(xs, ys):
    t_s = math.sqrt((xs/2) ** 2 + (ys/2) ** 2) * r.uniform(config.termination_score_min_max[0], config.termination_score_min_max[1])
    return t_s


class ChildErrorPackage:
    def __init__(self, error_type):
        self.error_type = "PARALLEL_SEGMENT_ERROR"


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
        if self.command == 'hard_right':
            return 90, 1000, 1
        else:
            print(f"Command not registered")



























