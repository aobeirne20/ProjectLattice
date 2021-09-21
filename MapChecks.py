import numpy as np
import math
from shapely.geometry import LineString, Point

import Map


def distance_between_point_and_seg(seg, loc):
    line = LineString([(seg.loc1[0], seg.loc1[1]), (seg.loc2[0], seg.loc2[1])])
    p = Point(loc.x, loc.y)
    d = p.distance(line)
    return d


def parallel_distance_between_seg_and_seg(seg1, seg2):
    if parallel_or_colinear_detector(seg1, seg2):
        if colinear_detector(seg1, seg2):
            return 0
        else:
            return parallel_distance(seg1, seg2)
    else:
        return float('inf')


def location_of_intersection_of_two_segs(seg1, seg2):
    if parallel_or_colinear_detector(seg1, seg2):
        return None
    else:
        line1 = LineString([(seg1.loc1[0], seg1.loc1[1]), (seg1.loc2[0], seg1.loc2[1])])
        line2 = LineString([(seg2.loc1[0], seg2.loc1[1]), (seg2.loc2[0], seg2.loc2[1])])
        intersection = line1.intersection(line2)
        if intersection.is_empty is False:
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



































