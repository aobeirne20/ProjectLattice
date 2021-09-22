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


def pick_start_loc(xs, ys):
    outer_rect_s = box(config.outer_rect[0][0] * xs, config.outer_rect[1][0] * ys, config.outer_rect[0][1] * xs, config.outer_rect[1][1] * ys)
    inner_rect_s = box(config.inner_rect[0][0] * xs, config.inner_rect[1][0] * ys, config.inner_rect[0][1] * xs, config.inner_rect[1][1] * ys)
    zone = np.random.choice(starting_zones, p=config.P_starting_zones) - 1
    zone_rect_s = box(config.zone_rects[zone][0][0] * xs, config.zone_rects[zone][0][1] * ys, config.zone_rects[zone][1][0] * xs, config.zone_rects[zone][1][1] * ys)

    valid = False
    while valid is not True:
        x = r.randint(0, xs)
        y = r.randint(0, ys)
        point = Point(x, y)
        if outer_rect_s.contains(point) is True and inner_rect_s.contains(point) is False and zone_rect_s.contains(point) is True:
            break
    return PositionAndDirection(x, y, None), zone


def check_start_loc(starting_location, map_network):
    if map_network.node_check(starting_location)["distance"] < config.starting_exclusion_scale:
        return False
    else:
        return True


def pick_start_dir(xs, ys, starting_location, zone):
    trend = np.random.choice(starting_zone_angles[zone], p=config.P_trend_chance[zone])
    angle = np.random.choice(starting_zone_angles[zone], p=config.P_angle_chance[zone])
    starting_location.dirc = angle
    return starting_location, trend


def check_start_dir(next_posdir, next_segment, map_network):
    if map_network.seg_parallel_check(next_segment)["distance"] < config.exclusion_scale:
        return False
    if map_network.node_check(next_posdir)["distance"] < config.exclusion_scale:
        return False
    else:
        return True


def create_straight(xs, ys, posdir, force_distance):
    if force_distance is None:
        next_distance = r.randint(int(xs / config.line_length_size_divisors[0]),
                                  int(ys / config.line_length_size_divisors[1]))
    else:
        next_distance = force_distance
    next_vector = (int(next_distance * straight_unit_vectors[posdir.dirc][0]),
                   int(next_distance * straight_unit_vectors[posdir.dirc][1]))
    next_posdir = PositionAndDirection(x=posdir.x + next_vector[0], y=posdir.y + next_vector[1], dirc=posdir.dirc)
    next_segment = ge.Segment(loc1=(posdir.x, posdir.y), loc2=(next_posdir.x, next_posdir.y), orientation=posdir.dirc)
    return next_posdir, next_segment, next_distance


def pick_next_curve(posdir, trend, force_change):
    # When the line is NOT ON TREND
    if force_change is None:
        if trend != posdir.dirc:
            change_s = np.random.choice(["Correct", "Random", "Continue"], p=config.P_chance_to_correct_random_continue)
            if change_s == "Correct":
                if angle_difference_abs(posdir.dirc, trend) > 45:
                    change_by = np.random.choice([45, 90], p=config.P_change_to_trend_by_amount_45_90)
                else:
                    change_by = 45
                if angle_difference_abs(posdir.dirc, trend) > 0:
                    next_posdir, curve = add_curve(posdir, posdir.dirc, change_by)
                elif angle_difference_abs(posdir.dirc, trend) < 0:
                    next_posdir, curve = add_curve(posdir, posdir.dirc, -1 * change_by)
            elif change_s == "Random":
                change = np.random.choice([-90, -45, 45, 90], p=config.P_curve_n90_n45_45_90_changes)
                next_posdir, curve = add_curve(posdir, posdir.dirc, change)
            elif change_s == "Continue":
                next_posdir = posdir
                curve = None

        # When the line is ON TREND
        elif trend == posdir.dirc:
            change_s = np.random.choice(["Random", "Continue"], p=config.P_chance_to_random_continue)
            if change_s == "Random":
                change = np.random.choice([-90, -45, 45, 90], p=config.P_curve_n90_n45_45_90_changes)
                next_posdir, curve = add_curve(posdir, posdir.dirc, change)
            elif change_s == "Continue":
                next_posdir = posdir
                curve = None
    else:
        next_posdir, curve = add_curve(posdir, posdir.dirc, force_change)
    return next_posdir, curve


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


def is_inside_boundaries(xs, ys, buffer1, buffer2):
    if buffer2[2].x + config.curve_scale*3 > (xs * config.boundaries[1]) or \
            buffer2[2].x - config.curve_scale * 3 < (xs * config.boundaries[0]) or \
            buffer2[2].y + config.curve_scale * 3 > (ys * config.boundaries[1]) or \
            buffer2[2].y - config.curve_scale * 3 < (ys * config.boundaries[0]):
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
    curve_location[0] + actual_curve_displacement[0] * config.curve_scale, curve_location[1] + actual_curve_displacement[1] * config.curve_scale)

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
    curve_location[0] + actual_curve_displacement[0] * config.curve_scale, curve_location[1] + actual_curve_displacement[1] * config.curve_scale)

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

def angle_difference_abs(ang1, ang2):
    # Without 360
    angc1 = ang2 - ang1
    if abs(angc1) > 180:
        angc1 = -1 * (360 - angc1)

    # With 360
    if ang1 == 0:
        ang1 = 360
    if ang2 == 0:
        ang2 = 360
    angc2 = ang2 - ang1
    if abs(angc2) > 180:
        angc2 = -1 * (360 - angc2)

    if abs(angc2) > abs(angc1):
        return angc1
    else:
        return angc2

