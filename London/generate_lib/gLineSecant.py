import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.TrackGeometry import Straight, Arc
from map_lib.Line import Line

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def gLineSecant(tmap, line_details):
    origin_spatial, anti_origin_spatial, trend, anti_trend = gen_origin(tmap)
    this_line = Line(origin_spatial, anti_origin_spatial, trend, anti_trend)
    # ORIGIN BRANCH

    # ANTI ORIGIN BRANCH
    # MUST FLIP TREND IN LINE FUNCTIONS



def gen_origin(tmap):
    # ADD INTERCHANGE STARTS LATER
    origin_x = np.random.randint(int(opt.secant_starting_bounds_x[0]*csg.xs), int(opt.secant_starting_bounds_x[1]*csg.xs))
    origin_y = np.random.randint(int(opt.secant_starting_bounds_y[0] * csg.ys), int(opt.secant_starting_bounds_y[1] * csg.ys))

    # PICK THE TREND
    if not tmap.secant_picked_dir:
        trend = np.random.choice(tmap.secant_not_picked_dir)
        tmap.secant_not_picked_dir.remove(trend)
        tmap.secant_picked_dir.append(trend)
    elif not tmap.secant_not_picked_dir:
        trend = np.random.choice(tmap.secant_picked_dir)
    else:
        if np.random.choice([True, False], p=opt.p_secant_pick_o_from_not_used_list):
            trend = np.random.choice(tmap.secant_not_picked_dir)
            tmap.secant_not_picked_dir.remove(trend)
            tmap.secant_picked_dir.append(trend)
        else:
            trend = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])

    # PICK THE ORIGIN DIRECTION
    trend = degree(trend)
    trend_change = np.random.choice([-3, -2, -1, 0, 1, 2, 3], p=opt.p_secant_start_off_trend)
    o = trend + trend_change

    origin_spatial = Spatial(x=origin_x, y=origin_y, o=degree(o))
    flip_spatial = Spatial(x=origin_x, y=origin_y, o=degree(o+4))
    flip_trend = trend + 4

    return origin_spatial, flip_spatial, trend, flip_trend



def genBranch(current_spatial: Spatial):



def r_frame_straight(this_line, current_spatial: Spatial):
    next_length = length_normal_dist()
    next_straight = Straight(current_spatial, next_length)
    return r_frame_curve(this_line, next_straight.spatial2)



def r_frame_curve(this_line, current_spatial: Spatial):
    next_curve_change = curve_change_choice(this_line, current_spatial)
    next_curve = Arc(current_spatial, next_curve_change, opt.cr_line)


def length_normal_dist():
    length = 0
    while not opt.b_secant_segment_length[0] < length < opt.b_secant_segment_length[1]:
        length = np.random.normal(loc=opt.secant_dist_params[0], scale=opt.secant_dist_params[1])
    return int(length)

def curve_change_choice(this_line: Line, current_spatial):
    # IF ON TREND
    if this_line.trend == current_spatial.o:
        arc_change = np.random.choice([-2, -1, 1, 2], p=opt.p_secant_on_trend_by)

    # IF NOT ON TREND
    else:
        if np.random.choice([True, False], p=opt.p_secant_return_to_trend):
            change_to_trend = current_spatial.o.change_to(this_line.trend)
            if abs(change_to_trend) == 1:
                arc_change = change_to_trend
            else:
                arc_change = np.random.choice([2, 1], p=opt.p_secant_off_trend_return_by)
                arc_change = arc_change * np.sign(change_to_trend)
        else:
            arc_change = np.random.choice([-2, -1, 1, 2], p=opt.p_secant_on_trend_by)
    return arc_change




