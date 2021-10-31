import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.StationGeometry import Station, Terminus
from geometry_lib.TrackGeometry import Straight, Arc
from map_lib.Line import Line
from London.generate_lib.line import gLineSecantHelpers

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def gLineSecant(tmap, line_details):
    origin_spatial, anti_origin_spatial, trend, anti_trend = gLineSecantHelpers.gen_origin(tmap)
    this_line = Line(origin_spatial, anti_origin_spatial, trend, anti_trend, line_details)
    origin_branch = this_line.form_origin_branch()
    anti_branch = this_line.form_anti_branch()

    # ORIGIN BRANCH
    frame_buffer = []
    error, frame_buffer = r_frame_straight(tmap, origin_branch, frame_buffer)
    gLineSecantHelpers.buffer_unload(tmap, this_line, frame_buffer)

    # ANTI ORIGIN BRANCH
    frame_buffer = []
    error, frame_buffer = r_frame_curve(tmap, anti_branch, frame_buffer)
    gLineSecantHelpers.buffer_unload(tmap, this_line, frame_buffer)

    return this_line


def r_frame_straight(tmap, this_branch, frame_buffer):
    attempts = 100
    while attempts >= 0:
        if not frame_buffer:
            current_spatial = this_branch.origin_spatial
        else:
            current_spatial = frame_buffer[-1].geometry.spatial2

        next_length = gLineSecantHelpers.length_normal_dist()
        next_straight = Straight(current_spatial, next_length)

        if next_straight.spatial2.x > (csg.xs*opt.b_map[1]) or next_straight.spatial2.x < (csg.xs*opt.b_map[0]) or \
            next_straight.spatial2.y > (csg.ys*opt.b_map[1]) or next_straight.spatial2.y < (csg.ys*opt.b_map[0]):
            if attempts > 0:
                attempts -= 100
                continue
            else:
                error, frame_buffer = r_terminus(tmap, this_branch, frame_buffer)
                return None, frame_buffer

        next_frame = gLineSecantHelpers.BufferFrame()
        next_frame.geometry = next_straight

        error, frame_buffer = r_frame_curve(tmap, this_branch, frame_buffer + [next_frame])
        return None, frame_buffer


def r_frame_curve(tmap, this_branch, frame_buffer):
    if not frame_buffer:
        current_spatial = this_branch.origin_spatial
    else:
        current_spatial = frame_buffer[-1].geometry.spatial2

    next_curve_change = gLineSecantHelpers.curve_change_choice(this_branch, current_spatial)
    next_curve = Arc(current_spatial, next_curve_change, opt.cr_line)

    next_frame = gLineSecantHelpers.BufferFrame()
    next_frame.geometry = next_curve

    error, frame_buffer = r_frame_straight(tmap, this_branch, frame_buffer + [next_frame])
    return None, frame_buffer


def r_terminus(tmap, this_branch, frame_buffer):
    frame_buffer.pop()
    end_frame = gLineSecantHelpers.BufferFrame()
    if not frame_buffer:
        station_spatial = this_branch.origin_spatial
    else:
        station_spatial = frame_buffer[-1].geometry.spatial2
    end_frame.stations.append(Terminus(station_spatial, True, opt.tick_length))
    return None, frame_buffer + [end_frame]





