import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.TrackGeometry import Straight, Arc
from map_lib.Line import Line
from London.generate_lib.line import gLineSecantHelpers

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def gLineSecant(tmap, line_details):
    origin_spatial, anti_origin_spatial, trend, anti_trend = gLineSecantHelpers.gen_origin(tmap)
    this_line = Line(origin_spatial, anti_origin_spatial, trend, anti_trend, line_details)

    line_buffer, station_buffer, interchange_buffer = [], [], []
    error, line_buffer, station_buffer, interchange_buffer = r_frame_straight(tmap, this_line, line_buffer, station_buffer, interchange_buffer)
    buffer_unload(tmap, this_line, line_buffer, station_buffer, interchange_buffer)

    # ANTI ORIGIN BRANCH
    # MUST FLIP TREND IN LINE FUNCTIONS
    return this_line



def r_frame_straight(tmap, this_line, line_buffer, station_buffer, interchange_buffer):
    if not line_buffer:
        current_spatial = this_line.origin_spatial
    else:
        current_spatial = line_buffer[-1].spatial2

    next_length = gLineSecantHelpers.length_normal_dist()
    next_straight = Straight(current_spatial, next_length)

    error, line_buffer, station_buffer, interchange_buffer = r_frame_curve(tmap, this_line,
                                                                           line_buffer + [next_straight],
                                                                           station_buffer,
                                                                           interchange_buffer)
    return None, line_buffer, station_buffer, interchange_buffer


def r_frame_curve(tmap, this_line, line_buffer, station_buffer, interchange_buffer):
    if not line_buffer:
        current_spatial = this_line.origin_spatial
    else:
        current_spatial = line_buffer[-1].spatial2

    next_curve_change = gLineSecantHelpers.curve_change_choice(this_line, current_spatial)
    next_curve = Arc(current_spatial, next_curve_change, opt.cr_line)

    error, line_buffer, station_buffer, interchange_buffer = r_terminus(tmap, this_line,
                                                                        line_buffer + [next_curve],
                                                                        station_buffer,
                                                                        interchange_buffer)
    return None, line_buffer, station_buffer, interchange_buffer


def r_terminus(tmap, this_line, line_buffer, station_buffer, interchange_buffer):
    return None, line_buffer, station_buffer, interchange_buffer


def buffer_unload(tmap, this_line, line_buffer, station_buffer, interchange_buffer):
    this_line.add_branch(line_buffer, station_buffer, interchange_buffer)


def buffer_package():
    pass



