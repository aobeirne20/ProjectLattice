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

        self.buffer = []
        self.P_branch = config.P_chance_of_branch_reverse_continue_choices[np.random.choice([0, 1, 2], p=config.P_branch_type_choice)]

    def generate(self):
        current_postdir, trend = self.origin()
        self.generate_branch(current_postdir, trend, config.termination_score)
        current_postdir, trend = self.reverse(trend)
        self.generate_branch(current_postdir, trend, config.termination_score)
        #self.terminate()
        for thing in self.buffer:
            if isinstance(thing[1], str) is not True:
                self.render_list.append(thing[1])
        return self.render_list

    def origin(self):
        # Choose between exisiting interchange, or new location
        potential_start_interchanges = lnh.potential_start_stations(xs=self.xs, ys=self.ys, map_network=self.map)
        chance = math.sqrt(len(potential_start_interchanges)*0.5)/8
        p_chance_to_start_on_int = [chance, 1-chance]
        if np.random.choice([True, False], p=p_chance_to_start_on_int) and potential_start_interchanges:
            origin_posdir = np.random.choice(potential_start_interchanges)
        else:
            origin_posdir = lnh.pick_start_loc(xs=self.xs, ys=self.ys)
            while lnh.check_start_loc(starting_location=origin_posdir, map_network=self.map) is False:
                origin_posdir = lnh.pick_start_loc(xs=self.xs, ys=self.ys)





        # Origin direction
        origin_posdir, trend = lnh.pick_start_dir(origin_posdir)
        # Flip for future reverse
        flip_dir = origin_posdir.dirc + 180
        if flip_dir >= 360:
            flip_dir -= 360
        # Append special origin to buffer
        self.buffer.append([lnh.PositionAndDirection(origin_posdir.x, origin_posdir.y, flip_dir), "Origin", origin_posdir])
        return origin_posdir, trend

    def generate_branch(self, current_postdir, trend, termination_score):
        force_change = None
        force_distance = None
        no_handle = False
        problem = False
        no_curve = False

        termination_check = 5
        while termination_score > 0:
            # Make the segment
            if no_curve is False:
                next_posdir, curve, change = lnh.pick_next_curve(current_postdir, trend, force_change=force_change)
            if no_curve is True:
                next_posdir = current_postdir
            next2_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, next_posdir, force_distance=force_distance)
            force_change = None
            force_distance = None
            no_curve = False

            # Check 1: End of Line Termination
            if lnh.is_inside_boundaries(xs=self.xs, ys=self.ys, postdir=next2_posdir) is False and termination_check > 0:
                termination_check -= 1
                continue
            if termination_check <= 0:
                break

            # Check 2: Incorrect sandwich check:

            # Check 3: Interchange Check
            crossings_from_seg = lnh.check_for_interchange_new_straight(next_segment, self.map)
            crossings_from_curve = None
            if curve is not None:
                crossings_from_curve = lnh.check_for_interchange_new_curve(curve, self.map)


            for crossing in crossings_from_seg:
                if crossing['object'] != 'LondonRiver':
                    if np.random.choice([True, False], p=config.P_seg_onto_seg):
                        if crossing['geometry'] == 'Arc45' or crossing['geometry'] == 'Arc90':
                            if np.random.choice([True, False], p=config.P_curve_onto_seg):
                                is_valid, do_add = lnh.check_for_interchange_dis(crossing['location'], self.map)
                                if is_valid and do_add:
                                    self.map.locus_list.append({"name": "Interchange", "location": crossing['location']})

                                    # Chance to terminate at interchange station
                                    if termination_score < config.low_termination_score * 2:
                                        force_change = change
                                        interchange_location = lnh.PositionAndDirection(x=crossing['location'][0], y=crossing['location'][1],
                                                                                        dirc=None)
                                        force_distance = interchange_location.distance_between(next_posdir)
                                        next2_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, next_posdir,
                                                                                                        force_distance=force_distance)

                                        termination_score = 0
                                        no_handle = True
                                elif is_valid is False:
                                    problem = True
                        else:
                            is_valid, do_add = lnh.check_for_interchange_dis(crossing['location'], self.map)
                            if is_valid and do_add:
                                self.map.locus_list.append({"name": "Interchange", "location": crossing['location']})

                                # Chance to terminate at interchange station
                                if termination_score < config.low_termination_score * 2:
                                    force_change = change
                                    interchange_location = lnh.PositionAndDirection(x=crossing['location'][0], y=crossing['location'][1], dirc=None)
                                    force_distance = interchange_location.distance_between(next_posdir)
                                    next2_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, next_posdir,
                                                                                                    force_distance=force_distance)

                                    termination_score = 0
                                    no_handle = True
                            elif is_valid is False:
                                problem = True

            if crossings_from_curve is not None:
                for crossing in crossings_from_curve:
                    if crossing['object'] != 'LondonRiver':
                        if crossing['geometry'] != 'Arc45' or crossing['geometry'] != 'Arc90':
                            self.map.locus_list.append({"name": "Interchange", "location": crossing['location']})






            # Append
            if problem is False:
                termination_score -= next_distance * r.randint(config.tscore[0], config.tscore[1])
                if curve is None:
                    self.buffer.append([current_postdir, 'Straight', next_posdir])
                else:
                    self.buffer.append([current_postdir, curve, next_posdir])
                self.buffer.append([next_posdir, next_segment, next2_posdir])
                current_postdir = next2_posdir
            elif problem is True:
                problem = False
                # Case 1: Previous segment. Easiest, pop twice from buffer then return.
                if len(self.buffer) > 2:
                    self.buffer.pop()
                    return_to = self.buffer.pop()
                    current_postdir =


                if bool(self.buffer) is False:
                    break
                previous = self.buffer.pop()
                previous_postdir = previous[0]
                next2_posdir, next_segment, next_distance = lnh.create_straight(self.xs, self.ys, previous_postdir,
                                                                                force_distance=None)
                no_curve = True
                force_distance = next_distance



            # Sub-branches
            branch_beh = np.random.choice(["Branch", "Reverse", "Continue"], p=self.P_branch)
            if branch_beh == "Branch":
                branch_code = np.random.choice(config.branch_codes, p=config.P_branch_trend_change)
                branch_trend = lnh.orientation_change(trend, branch_code["trend_change"])
                branch_angle_change = np.random.choice(branch_code["angle_changes"], p=branch_code["angle_changes_P"])
                branch_postdir, curve = lnh.add_curve(posdir=current_postdir, current_direction=current_postdir.dirc, change=branch_angle_change)
                self.buffer.append([current_postdir, curve, branch_postdir])
                self.generate_branch(branch_postdir, branch_trend, r.randint(int(config.termination_score/config.branch_t_f), config.termination_score))

        # Make the end of line handle:
        if no_handle is False:
            self.buffer.append






    def reverse(self, trend):
        trend = trend + 180
        if trend >= 360:
            trend -= 360
        return self.buffer[0][0], trend































