import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg

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
        if np.random.choice(opt.v_secant_pick_o_from_not_used_list, p=opt.p_secant_pick_o_from_not_used_list):
            trend = np.random.choice(tmap.secant_not_picked_dir)
            tmap.secant_not_picked_dir.remove(trend)
            tmap.secant_picked_dir.append(trend)
        else:
            trend = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])

    # PICK THE ORIGIN DIRECTION
    trend = degree(trend)
    trend_change = np.random.choice(opt.v_secant_start_off_trend, p=opt.p_secant_start_off_trend)
    o = trend + trend_change

    origin_spatial = Spatial(x=origin_x, y=origin_y, o=degree(o))
    flip_spatial = Spatial(x=origin_x, y=origin_y, o=degree(o+4))
    flip_trend = trend + 4

    return origin_spatial, flip_spatial, trend, flip_trend


def length_normal_dist():
    length = 0
    while not opt.b_secant_segment_length[0] < length < opt.b_secant_segment_length[1]:
        length = np.random.normal(loc=opt.std_secant_segment_length[0], scale=opt.std_secant_segment_length[1])
    return int(length * opt.s)


def curve_change_choice(this_line, current_spatial):
    # IF ON TREND
    if this_line.trend == current_spatial.o:
        arc_change = np.random.choice(opt.v_secant_on_trend_diverge_by, p=opt.p_secant_on_trend_diverge_by)

    # IF NOT ON TREND
    else:
        change_to_trend = current_spatial.o.change_to(this_line.trend)
        if abs(change_to_trend) == 1:
            p_secant_return_to_trend = opt.p_secant_return_to_trend_off_by_1
        elif abs(change_to_trend) == 2:
            p_secant_return_to_trend = opt.p_secant_return_to_trend_off_by_2
        elif abs(change_to_trend) == 3:
            p_secant_return_to_trend = opt.p_secant_return_to_trend_off_by_3
        else:
            raise ValueError("This should never happen!")
        if np.random.choice([True, False], p=p_secant_return_to_trend):
            if abs(change_to_trend) == 1:
                arc_change = change_to_trend
            else:
                arc_change = np.random.choice([2, 1], p=opt.p_secant_off_trend_return_by)
                arc_change = arc_change * np.sign(change_to_trend)
        else:
            if abs(change_to_trend) > 2:
                arc_change = np.random.choice([-1, 1])
            else:
                arc_change = np.random.choice(opt.v_secant_on_trend_diverge_by, p=opt.p_secant_on_trend_diverge_by)

    # No diagonal 90 changes
    if abs(arc_change) > 1 and current_spatial.o % 2 != 0:
        arc_change = 1 * np.sign(arc_change)

    # No changes from 2 -> 4:
    if abs(degree(current_spatial.o + arc_change).change_to(this_line.trend)) >= 4:
        arc_change = 1 * np.sign(arc_change)

    return arc_change


def buffer_unload(tmap, this_line, frame_buffer):
    this_line.add_branch(frame_buffer)


class BufferFrame:
    def __init__(self):
        self.geometry = None
        self.stations = []
        self.interchanges = []
        self.sandwiches = []