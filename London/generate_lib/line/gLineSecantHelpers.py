import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.StationGeometry import Station, Terminus
from geometry_lib.SpecialGeometry import TextBox

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def gen_origin(tmap):
    # ADD INTERCHANGE STARTS LATER
    origin_x = np.random.randint(int(opt.secant_starting_bounds_x[0]*csg.xs), int(opt.secant_starting_bounds_x[1]*csg.xs))
    origin_y = np.random.randint(int(opt.secant_starting_bounds_y[0] * csg.ys), int(opt.secant_starting_bounds_y[1] * csg.ys))

    # PICK THE TREND
    # True if Picked is EMPTY
    if not tmap.secant_picked_dir:
        trend = np.random.choice(tmap.secant_not_picked_dir)
    # True if Not Picked is EMPTY
    elif not tmap.secant_not_picked_dir:
        trend = np.random.choice(tmap.secant_picked_dir)
    else:
        if np.random.choice(opt.v_secant_pick_o_from_not_used_list, p=opt.p_secant_pick_o_from_not_used_list):
            trend = np.random.choice(tmap.secant_not_picked_dir)
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


def curve_change_choice(current_trend, current_spatial):
    # IF ON TREND
    if current_trend == current_spatial.o:
        arc_change = np.random.choice(opt.v_secant_on_trend_diverge_by, p=opt.p_secant_on_trend_diverge_by)

    # IF NOT ON TREND
    else:
        change_to_trend = current_spatial.o.change_to(current_trend)
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
    if abs(degree(current_spatial.o + arc_change).change_to(current_trend)) >= 4:
        arc_change = 1 * np.sign(arc_change)

    return arc_change


def get_terminus_station(end_frame, texterator, station_type):
    for station in end_frame.stations:
        print(type(station))
        if type(station) is Terminus:
            end_frame.labels.append(TextBox(spatial_station=station.spatial_station,
                                            text=texterator.get_name(station_type)[0],
                                            offset=0, font_name=opt.station_font, font_size=opt.station_text_size, special_fix=None))
    return end_frame




def gen_stations(next_frame, texterator, station_type):
    len_to_min_distance_dict = {0: 26, 1: 26, 2: 18, 3: 26, 4: 26, 5: 26, 6: 18, 7: 26}
    seg_length = next_frame.geometry.logic_manifold.length
    min_sep = len_to_min_distance_dict[next_frame.geometry.spatial1.o] * opt.s
    # SEGMENT TOO SMALL
    if seg_length < min_sep * 1.5:
        return next_frame
    # SEGMENT CAN FIT STATIONS
    if np.random.choice([True, False], p=[0.9, 0.1]):  #Fit ANY Stations
        current_position_along_segment = 0
        _, next_frame = gen_stations_recursor(current_position_along_segment, seg_length, min_sep, next_frame, texterator, station_type)
    return next_frame


def gen_stations_recursor(current_pos, seg_length, min_sep, next_frame, texterator, station_type):
    sep = station_normal_dist(min_sep=min_sep, max_sep=seg_length*0.75)
    initial_break = np.random.randint(0.1*sep, 1*sep)
    current_pos = current_pos + initial_break

    while current_pos < seg_length:
        if np.random.choice([True, False], p=[0.95, 0.05]):
            x = next_frame.geometry.spatial1.x + next_frame.geometry.spatial1.o.ux * current_pos
            y = next_frame.geometry.spatial1.y + next_frame.geometry.spatial1.o.uy * current_pos
            o = next_frame.geometry.spatial1.o

            names_spacing_list = texterator.get_name(station_type)

            if o == 0 or o == 4:
                if len(names_spacing_list) > 1:
                    name = names_spacing_list[1]
                else:
                    name = names_spacing_list[0]
            else:
                name = names_spacing_list[0]


            next_frame.stations.append(Station(spatial1=Spatial(x, y, o), opposite=False, tick_length=opt.tick_length))
            next_frame.labels.append(TextBox(spatial_station=next_frame.stations[-1].spatial_station,
                                             text=name,
                                             offset=0, font_name=opt.station_font, font_size=opt.station_text_size, special_fix=None))
        current_pos += sep
        if np.random.choice([True, False], p=[0.5, 0.5]):
            current_pos, next_frame = gen_stations_recursor(current_pos, seg_length, min_sep, next_frame, texterator, station_type)
            break
    return current_pos, next_frame


def station_normal_dist(min_sep, max_sep):
    sep = 0
    while not min_sep < sep < max_sep:
        sep = np.random.normal(loc=(min_sep + max_sep)/2, scale=(min_sep + max_sep)/4)
    return int(sep)





class BufferFrame:
    def __init__(self, geometry=None):
        if geometry is None:
            self.geometry = None
        else:
            self.geometry = geometry
        self.stations = []
        self.interchanges = []
        self.sandwiches = []
        self.labels = []


