import numpy as np
import random as r
import math

from LineGenerators import LG1_Config as config
import geometric_elements as ge
from shapely.geometry import Point, Polygon, box

# ZONES
# 1 2 3
# 4 5 6

starting_zones = [1, 2, 3, 4, 5, 6]
starting_zone_angles = [[270, 315, 0], [225, 270, 315], [180, 225, 270], [0, 45, 90], [135, 90, 45], [90, 135, 180]]
starting_zone_trends = [[270, 315, 0], [225, 270, 315], [180, 225, 270], [0, 45, 90], [135, 90, 45], [90, 135, 180]]


slz = [[1 / 20, 1 / 4], [3 / 4, 19 / 20]]

straight_unit_vectors = {0: (1, 0), 45: (math.sqrt(0.5), -1 * math.sqrt(0.5)), 90: (0, -1), 135: (-1 * math.sqrt(0.5), -1 * math.sqrt(0.5)),
                         180: (-1, 0), 225: (-1 * math.sqrt(0.5), math.sqrt(0.5)), 270: (0, 1), 315: (math.sqrt(0.5), math.sqrt(0.5)), 360: (1, 0)}

rd_to_curve_displacer = {315: 0, 45: 90, 135: 180, 225: 270}
ld_to_curve_displacer = {}
curve_displacement = {90: np.array(([1], [-1])), -90: np.array(([1], [1])), 45: np.array(([2], [-1])), -45: np.array(([2], [1]))}
curve_displacement_dx = {45: np.array(([1], [-2])), -45: np.array(([1], [2]))}
rotate_array_dict = {90: np.array(([0, 1], [-1, 0])), -90: np.array(([0, -1], [1, 0])),
                     45: np.array(([0, math.sqrt(0.5)], [-1 * math.sqrt(0.5), 0])), -45: np.array(([0, -1 * math.sqrt(0.5)], [math.sqrt(0.5), 0]))}
rotate_instructions = {0: [], 45: [45], 90: [90], 135: [90, 45], 180: [90, 90], 225: [90, 90, 45], 270: [90, 90, 90], 315: [90, 90, 90, 45]}


class PositionAndDirection:
    def __init__(self, x, y, dirc):
        self.x = x
        self.y = y
        self.dirc = dirc
        if self.dirc is not None:
            if self.dirc >= 360:
                self.dirc -= 360
            elif self.dirc < 0:
                self.dirc += 360

    def orientation_change(self, change):
        direction = self.dirc + change
        if direction >= 360:
            direction -= 360
        elif direction < 0:
            direction += 360
        self.dirc = direction
        return self.dirc

    def distance_between(self, posdir2):
        loc1 = np.asarray([self.x, self.y])
        loc2 = np.asarray([posdir2.x, posdir2.y])
        return np.linalg.norm(loc1-loc2)


def pick_start_loc(xs, ys):
    x = r.randint(int(config.x_box[0] * xs), int(config.x_box[1] * xs))
    y = r.randint(int(config.y_box[0] * ys), int(config.y_box[1] * ys))
    return PositionAndDirection(x, y, None)


def pick_start_dir(starting_location):
    trend = np.random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    change = np.random.choice([-45, 0, 45], p=config.P_chance_to_start_n45_on_45)
    starting_location.dirc = orientation_change(trend, change)
    return starting_location, trend


def potential_start_stations(xs, ys, map_network):
    all_locs = []
    if map_network.locus_list is False:
        return all_locs
    else:
        for station in map_network.locus_list:
            if station['name'] == 'Interchange':
                test_postdir = PositionAndDirection(x=station['location'][0], y=station['location'][1], dirc=None)
                if is_inside_starting_boundaries(xs, ys, test_postdir):
                    all_locs.append(test_postdir)
    return all_locs


def create_straight(xs, ys, posdir, force_distance, mod_distance_f):
    if force_distance is None:
        next_distance = r.randint(int(xs / config.line_length_size_divisors[0]),
                                  int(ys / config.line_length_size_divisors[1]))
    else:
        next_distance = force_distance
    if mod_distance_f is None:
        pass
    else:
        next_distance = next_distance * mod_distance_f
    next_vector = (int(next_distance * straight_unit_vectors[posdir.dirc][0]),
                   int(next_distance * straight_unit_vectors[posdir.dirc][1]))
    next_posdir = PositionAndDirection(x=posdir.x + next_vector[0], y=posdir.y + next_vector[1], dirc=posdir.dirc)
    next_segment = ge.Segment(loc1=(posdir.x, posdir.y), loc2=(next_posdir.x, next_posdir.y), orientation=posdir.dirc, dis=next_distance)
    return next_posdir, next_segment, next_distance


def pick_next_curve(posdir, trend, force_change):
    # When the line is NOT ON TREND
    if force_change is None:
        if trend != posdir.dirc:
            change_s = np.random.choice(["Correct", "Random", "Continue"], p=config.P_chance_to_correct_random_continue)
            if change_s == "Correct":
                angle_diff = angle_difference(posdir.dirc, trend)
                if abs(angle_diff) > 45:
                    change = np.random.choice([45, 90], p=config.P_change_to_trend_by_amount_45_90)
                else:
                    change = 45
                if angle_diff > 0:
                    next_posdir, curve = add_curve(posdir, posdir.dirc, change)
                elif angle_diff < 0:
                    next_posdir, curve = add_curve(posdir, posdir.dirc, -1 * change)

            elif change_s == "Random":
                change = np.random.choice([-90, -45, 45, 90], p=config.P_curve_n90_n45_45_90_changes)
                next_posdir, curve = add_curve(posdir, posdir.dirc, change)
            elif change_s == "Continue":
                next_posdir = posdir
                change = None
                curve = None


        # When the line is ON TREND
        elif trend == posdir.dirc:
            change_s = np.random.choice(["Random", "Continue"], p=config.P_chance_to_random_continue)
            if change_s == "Random":
                change = np.random.choice([-90, -45, 45, 90], p=config.P_curve_n90_n45_45_90_changes)
                next_posdir, curve = add_curve(posdir, posdir.dirc, change)
            elif change_s == "Continue":
                next_posdir = posdir
                change = None
                curve = None
    elif force_change == 0:
        next_posdir = posdir
        change = None
        curve = None
    else:
        next_posdir, curve = add_curve(posdir, posdir.dirc, force_change)
        change = force_change
    return next_posdir, curve, change


def check_start_loc(starting_location, map_network):
    if map_network.node_check(starting_location)["distance"] < config.starting_exclusion_scale:
        return False
    else:
        return True


def check_start_dir(next_posdir, next_segment, map_network):
    if map_network.seg_parallel_check(next_segment)["distance"] < config.exclusion_scale:
        return False
    if map_network.node_check(next_posdir)["distance"] < config.exclusion_scale:
        return False
    else:
        return True


def check_for_interchange_new_straight(next_segment, map_network):
    return map_network.seg_crossing_check(next_segment)


def check_for_interchange_new_curve(next_curve, map_network):
    return map_network.seg_crossing_check(next_curve)

def check_for_any_collision(part, map_network):
    crossing_dict = map_network.seg_crossing_check(part)
    object_list = []
    for c in crossing_dict:
        object_list.append(c['object'])
    if crossing_dict is not None:
        return True, object_list
    else:
        return False, None

def wrong_sandwich(next_segment, map_network):
    seg_parallel_check = map_network.seg_parallel_check(next_segment)
    if seg_parallel_check["distance"] < config.parallel_exclusion_scale:
        return seg_parallel_check
    else:
        return None

def check_for_interchange_dis(location, map_network):
    if map_network.interchange_dist_check(location[0], location[1]) < config.interchange_exclusion_scale/100:
        return True, False
    elif map_network.interchange_dist_check(location[0], location[1]) < config.interchange_exclusion_scale:
        return False, False
    else:
        return True, True

def check_next_curve(xs, ys, next_posdir, next_curve, map_network):
    if next_posdir.x > (xs * config.boundaries[1]) or next_posdir.x < (xs * config.boundaries[0]) or \
            next_posdir.y > (ys * config.boundaries[1]) or next_posdir.y < (ys * config.boundaries[0]):
        return False
    if map_network.seg_parallel_check(next_curve)["distance"] < config.exclusion_scale:
        return False
    if map_network.node_check(next_posdir)["distance"] < config.exclusion_scale:
        return False
    else:
        return True


def check_next_segment(xs, ys, next_posdir, next_segment, map_network):
    if next_posdir.x > (xs * config.boundaries[1]) or next_posdir.x < (xs * config.boundaries[0]) or \
            next_posdir.y > (ys * config.boundaries[1]) or next_posdir.y < (ys * config.boundaries[0]):
        return "BoundaryTerm", None
    check1 = map_network.seg_parallel_check(next_segment)
    if check1["distance"] < config.exclusion_scale:
        return "NewCurve", None
    check2 = map_network.node_check(next_posdir)
    if check2["distance"] < config.exclusion_scale:
        return "NewSegment", None
    check3 = map_network.seg_crossing_check(next_segment)
    if check3 is not None:
        return "NewInterchange", check3
    return None, None


def is_inside_boundaries(xs, ys, postdir):
    if postdir.x + config.curve_scale > xs * config.boundaries[1] or \
        postdir.x - config.curve_scale < xs * config.boundaries[0] or \
        postdir.y + config.curve_scale > ys * config.boundaries[1] or \
        postdir.y - config.curve_scale < ys * config.boundaries[0]:
        return False
    else:
        return True

def is_inside_starting_boundaries(xs, ys, postdir):
    if postdir.x + config.curve_scale > xs * config.x_box[1] or \
        postdir.x - config.curve_scale < xs * config.x_box[0] or \
        postdir.y + config.curve_scale > ys * config.y_box[1] or \
        postdir.y - config.curve_scale < ys * config.y_box[0]:
        return False
    else:
        return True



# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
def add_curve(posdir, current_direction, change):
    if current_direction == 0 or current_direction == 90 or current_direction == 180 or current_direction == 270:
        next_location, next_direction, curve = add_curve_to_90((posdir.x, posdir.y), current_direction, change)

    if current_direction == 45 or current_direction == 135 or current_direction == 225 or current_direction == 315:
        next_location, next_direction, curve = add_curve_to_45((posdir.x, posdir.y), current_direction, change)

    next_posdir = PositionAndDirection(x=next_location[0], y=next_location[1], dirc=next_direction)
    return next_posdir, curve


def add_curve_to_90(curve_location, current_direction, change):
    typ_curve_displacement = curve_displacement[change]
    for instruction in rotate_instructions[current_direction]:
        typ_curve_displacement = np.matmul(rotate_array_dict[instruction], typ_curve_displacement)
    actual_curve_displacement = typ_curve_displacement
    loc2 = (
    curve_location[0] + actual_curve_displacement[0][0] * config.curve_scale, curve_location[1] + actual_curve_displacement[1][0] * config.curve_scale)

    if change == 90:
        curve = ge.Arc90(loc1=curve_location, loc2=loc2, orientation=current_direction, chirality='L', curve_scale=config.curve_scale)
    elif change == 45:
        curve = ge.Arc45(loc1=curve_location, loc2=loc2, orientation=current_direction, chirality='Ls', curve_scale=config.curve_scale)
    elif change == -45:
        curve = ge.Arc45(loc1=curve_location, loc2=loc2, orientation=current_direction, chirality='Rs', curve_scale=config.curve_scale)
    elif change == -90:
        curve = ge.Arc90(loc1=curve_location, loc2=loc2, orientation=current_direction, chirality='R', curve_scale=config.curve_scale)

    return loc2, orientation_change(current_direction, change), curve


def add_curve_to_45(curve_location, current_direction, change):
    if change == -90 or change == -45:
        change = -45
        mod_direction = orientation_change(current_direction, 45)
    elif change == 90 or change == 45:
        change = 45
        mod_direction = orientation_change(current_direction, -45)

    typ_curve_displacement = curve_displacement_dx[change]
    for instruction in rotate_instructions[mod_direction]:
        typ_curve_displacement = np.matmul(rotate_array_dict[instruction], typ_curve_displacement)
    actual_curve_displacement = typ_curve_displacement
    loc2 = (
    curve_location[0] + actual_curve_displacement[0][0] * config.curve_scale, curve_location[1] + actual_curve_displacement[1][0] * config.curve_scale)

    if change == 45:
        curve = ge.Arc45(loc1=curve_location, loc2=loc2, orientation=orientation_change(current_direction, -45), chirality='Ld',
                         curve_scale=config.curve_scale)
    elif change == -45:
        curve = ge.Arc45(loc1=curve_location, loc2=loc2, orientation=orientation_change(current_direction, 45), chirality='Rd',
                         curve_scale=config.curve_scale)

    return loc2, orientation_change(current_direction, change), curve


def orientation_change(base_dir, change_dir):
    direction = base_dir + change_dir
    if direction >= 360:
        direction -= 360
    elif direction < 0:
        direction += 360
    return direction

def angle_difference(from_ang, to_ang):
    # in direction of increasing degrees
    if to_ang < from_ang:
        increasing_change = (to_ang + 360) - from_ang
    else:
        increasing_change = (to_ang) - from_ang

     # in direction of decreasing degrees
    if to_ang > from_ang:
        decreasing_change = (from_ang + 360) - to_ang
    else:
        decreasing_change = (from_ang) - to_ang

    if increasing_change == decreasing_change:
        return np.random.choice([-180, 180])
    elif increasing_change < decreasing_change:
        return increasing_change
    elif decreasing_change < increasing_change:
        return -1 * decreasing_change
    else:
        return 0


