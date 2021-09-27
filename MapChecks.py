import numpy as np
import math
from shapely.geometry import LineString, Point
from matplotlib import pyplot

import geometric_elements as ge

import Map




def distance_between_point_and_seg(seg, loc):
    line = LineString([(seg.loc1[0], seg.loc1[1]), (seg.loc2[0], seg.loc2[1])])
    p = Point(loc.x, loc.y)
    d = p.distance(line)
    return d


def parallel_distance_between_seg_and_seg(seg1, seg2):
    if isinstance(seg1, ge.Segment):
        if is_parallel(seg1, seg2):
            line1 = LineString([(seg1.loc1[0], seg1.loc1[1]), (seg1.loc2[0], seg1.loc2[1])])
            line2 = LineString([(seg2.loc1[0], seg2.loc1[1]), (seg2.loc2[0], seg2.loc2[1])])
            return line1.distance(line2)
    return float('inf')


def is_parallel(seg1, seg2):
    ang1 = seg1.orientation
    ang2 = seg2.orientation
    if ang1 == ang2 or ang1 + 180 == ang2 or ang1 - 180 == ang2:
        return True
    else:
        return False





def location_of_intersection_of_two_segs(seg1, seg2):
    lines = []
    for seg in [seg1, seg2]:
        # Defining different segments
        if isinstance(seg, ge.Segment):
            line1 = LineString([(seg.loc1[0], seg.loc1[1]), (seg.loc2[0], seg.loc2[1])])
        elif isinstance(seg, ge.Arc90):
            centerx = seg.center[0]
            centery = seg.center[1]
            radius = seg.curve_scale
            if seg.chirality == 'R':
                start_angle = -1*(seg.orientation + 90)
                end_angle = -1*seg.orientation
            elif seg.chirality == 'L':
                start_angle = -1*(seg.orientation - 90)
                end_angle = -1*seg.orientation
            numsegments = 100

            theta = np.radians(np.linspace(start_angle, end_angle, numsegments))
            x = centerx + radius * np.cos(theta)
            y = centery + radius * np.sin(theta)

            line1 = LineString(np.column_stack([x, y]))



        elif isinstance(seg, ge.Arc45):
            line_coords = np.asarray([[seg.intro_seg[0], seg.intro_seg[1]]])

            centerx = seg.center[0]
            centery = seg.center[1]
            radius = seg.curve_scale
            if seg.chirality == 'Rs':
                start_angle = -1*(seg.orientation + 45)
                end_angle = -1*(seg.orientation + 90)
            elif seg.chirality == 'Ls':
                start_angle = -1*(seg.orientation - 45)
                end_angle = -1*(seg.orientation - 90)
            elif seg.chirality == 'Rd':
                start_angle = -1*(seg.orientation)
                end_angle = -1*(seg.orientation + 45)
            elif seg.chirality == 'Ld':
                start_angle = -1*(seg.orientation)
                end_angle = -1*(seg.orientation - 45)
            numsegments = 100

            theta = np.radians(np.linspace(start_angle, end_angle, numsegments))
            x = centerx + radius * np.cos(theta)
            y = centery + radius * np.sin(theta)

            arc_coords = np.column_stack(np.asarray([x, y]))
            line_coords = np.concatenate([arc_coords, line_coords])
            line_coords = np.concatenate([np.asarray([[seg.outro_seg[2], seg.outro_seg[3]]]), line_coords])

            line1 = LineString(line_coords)

        lines.append(line1)

    intersection = lines[0].intersection(lines[1])

    if intersection.is_empty is False:
        if isinstance(intersection, Point):
            i_tp = (int(intersection.x), int(intersection.y))
            return i_tp
    else:
        return None


def parallel_or_colinear_detector(seg1, seg2):
    if seg1.orientation == seg2.orientation or \
            seg1.orientation - 180 == seg2.orientation or \
            seg1.orientation + 180 == seg2.orientation:
        return True
    else:
        return False


def parallel_distance(seg1, seg2):
    if seg1.orientation == 0 or seg1.orientation == 180:
        return abs(seg1.loc1[1] - seg2.loc1[1])
    elif seg1.orientation == 90 or seg1.orientation == 270:
        return abs(seg1.loc1[0] - seg2.loc1[0])
    elif seg1.orientation == 45 or seg1.orientation == 225:
        intercept1 = seg1.loc1[1] + seg1.loc1[0]
        intercept2 = seg2.loc1[1] + seg2.loc1[0]
        x = abs(intercept2 - intercept1) / 2
        return math.sqrt(x ** 2 + x ** 2)
    elif seg1.orientation == 135 or seg1.orientation == 315:
        intercept1 = seg1.loc1[1] - seg1.loc1[0]
        intercept2 = seg2.loc1[1] - seg2.loc1[0]
        x = abs(intercept2 - intercept1) / 2
        return math.sqrt(x ** 2 + x ** 2)


def colinear_detector(seg1, seg2):
    if seg1.orientation == 0 or seg1.orientation == 180:
        if seg1.loc1[1] == seg2.loc1[1]:
            return True
    elif seg1.orientation == 90 or seg1.orientation == 270:
        if seg1.loc1[0] == seg2.loc1[0]:
            return True
    elif seg1.orientation == 45 or seg1.orientation == 225:
        intercept1 = seg1.loc1[1] + seg1.loc1[0]
        intercept2 = seg2.loc1[1] + seg2.loc1[0]
        if intercept1 == intercept2:
            return True
    elif seg1.orientation == 135 or seg1.orientation == 315:
        intercept1 = seg1.loc1[1] - seg1.loc1[0]
        intercept2 = seg2.loc1[1] - seg2.loc1[0]
        if intercept1 == intercept2:
            return True
    else:
        return False



































