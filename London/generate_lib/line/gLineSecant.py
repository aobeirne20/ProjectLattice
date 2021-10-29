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

    frame_buffer = []
    error, frame_buffer = r_frame_straight(tmap, this_line, frame_buffer)
    gLineSecantHelpers.buffer_unload(tmap, this_line, frame_buffer)

    # ANTI ORIGIN BRANCH
    this_line.flip_for_anti_branch()
    frame_buffer = []
    error, frame_buffer = r_frame_straight(tmap, this_line, frame_buffer)
    gLineSecantHelpers.buffer_unload(tmap, this_line, frame_buffer)

    return this_line


def r_frame_straight(tmap, this_line, frame_buffer):
    if not frame_buffer:
        current_spatial = this_line.origin_spatial
    else:
        current_spatial = frame_buffer[-1].geometry.spatial2

    next_length = gLineSecantHelpers.length_normal_dist()
    next_straight = Straight(current_spatial, next_length)

    if next_straight.spatial2.x > csg.xs or next_straight.spatial2.x < 0 or next_straight.spatial2.y > csg.ys or next_straight.spatial2.y < 0:
        error, frame_buffer = r_terminus(tmap, this_line, frame_buffer)
        return None, frame_buffer

    next_frame = gLineSecantHelpers.BufferFrame()
    next_frame.geometry = next_straight

    error, frame_buffer = r_frame_curve(tmap, this_line, frame_buffer + [next_frame])
    return None, frame_buffer


def r_frame_curve(tmap, this_line, frame_buffer):
    if not frame_buffer:
        current_spatial = this_line.origin_spatial
    else:
        current_spatial = frame_buffer[-1].geometry.spatial2

    next_curve_change = gLineSecantHelpers.curve_change_choice(this_line, current_spatial)
    next_curve = Arc(current_spatial, next_curve_change, opt.cr_line)

    next_frame = gLineSecantHelpers.BufferFrame()
    next_frame.geometry = next_curve

    error, frame_buffer = r_frame_straight(tmap, this_line, frame_buffer + [next_frame])
    return None, frame_buffer


def r_terminus(tmap, this_line, frame_buffer):
    return None, frame_buffer





