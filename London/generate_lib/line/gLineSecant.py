import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.StationGeometry import Station, Terminus
from geometry_lib.InterchangeGeometry import InterchangeNode, InterchangeConnector, DarkNode
from geometry_lib.TrackGeometry import Straight, Arc
from map_lib.Line import Line
from London.generate_lib.line import gLineSecantHelpers

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg

class gLineSecant():
    def __init__(self, tmap, line_details, texterator):
        self.tmap = tmap
        self.this_line = Line(line_details)
        self.this_branch = None
        self.texterator = texterator
        self.sub_branches = []

        self.branch_buffers = []


        prime_error = "origin"
        # ORIGIN BRANCH
        while error is not None:
            self.this_line.set_origin_details(*gLineSecantHelpers.gen_origin(tmap))
            self.this_branch, frame_buffer = self.this_line.give_origin_branch(), []
            error, frame_buffer = self.r_frame_straight(frame_buffer)
        self.save_this_branch_buffer(frame_buffer)

        # ANTI ORIGIN BRANCH
        self.this_line.randomize_anti_trend()
        self.this_branch, frame_buffer = self.this_line.give_anti_branch(), []
        error, frame_buffer = self.r_frame_curve(frame_buffer)
        self.save_this_branch_buffer(frame_buffer)

        # SUB-BRANCHES
        for branch in self.this_line.sub_branch_starters:
            self.this_branch, frame_buffer = branch, []
            error, frame_buffer = self.r_frame_straight(frame_buffer)
            self.save_this_branch_buffer(frame_buffer)

    def return_line(self):
        self.this_line.unload_branch_buffer(self.branch_buffers)
        return self.this_line

    def save_this_branch_buffer(self, frame_buffer):
        self.branch_buffers.append([frame_buffer, self.this_branch])

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

    # Recursive frame that creates straights
    def r_frame_straight(self, frame_buffer):
        attempts = 100
        while attempts >= 0:
            if not frame_buffer:
                current_spatial = self.this_branch.origin_spatial
            else:
                current_spatial = frame_buffer[-1].geometry.spatial2

            next_length = gLineSecantHelpers.length_normal_dist()
            next_straight = Straight(current_spatial, next_length)
            next_frame = gLineSecantHelpers.BufferFrame()
            next_frame.geometry = next_straight

            error, next_frame = self.line_collision_check(next_frame, frame_buffer, current_spatial)
            if error is not None:
                continue

            if self.tmap.distance_to_edge(next_straight) <= opt.map_border_buffer:
                if attempts > 0:
                    attempts -= 50
                    continue
                else:
                    error, frame_buffer = self.r_terminus(frame_buffer)
                    return None, frame_buffer

            next_frame = gLineSecantHelpers.gen_stations(next_frame, self.texterator, self.this_line.style_details['station_type'])

            error, frame_buffer = self.r_frame_curve(frame_buffer + [next_frame])
            if error is not None:
                attempts -= 50
                continue
            else:
                return None, frame_buffer
        return "big_error", frame_buffer

    # Recursive frame that creates arcs
    def r_frame_curve(self, frame_buffer):
        attempts = 100
        while attempts >= 0:
            if not frame_buffer:
                current_spatial = self.this_branch.origin_spatial
            else:
                current_spatial = frame_buffer[-1].geometry.spatial2

            next_curve_change = gLineSecantHelpers.curve_change_choice(self.this_branch.trend, current_spatial)
            next_curve = Arc(current_spatial, next_curve_change, opt.cr_line)
            next_frame = gLineSecantHelpers.BufferFrame()
            next_frame.geometry = next_curve

            error, next_frame = self.line_collision_check(next_frame, frame_buffer, current_spatial)

            if self.tmap.distance_to_edge(next_curve) <= opt.map_border_buffer:
                if attempts > 0:
                    attempts -= 50
                    continue
                else:
                    error, frame_buffer = self.r_terminus(frame_buffer)
                    return None, frame_buffer

            error, frame_buffer = self.r_frame_straight(frame_buffer + [next_frame])
            if error is not None:
                continue
            else:
                return None, frame_buffer
        return "big_error", frame_buffer

    # Recursive frame that ends the line
    def r_terminus(self, frame_buffer):
        if not frame_buffer:
            current_spatial = self.this_branch.origin_spatial
        else:
            current_spatial = frame_buffer[-1].geometry.spatial2

        next_frame = gLineSecantHelpers.BufferFrame()
        next_frame.geometry = Straight(current_spatial, np.random.randint(opt.b_secant_segment_length[0], self.tmap.point_distance_to_edge(current_spatial)-100))

        end_frame = gLineSecantHelpers.BufferFrame()
        end_frame.geometry = Straight(next_frame.geometry.spatial2, 50)
        end_frame.stations.append(Terminus(end_frame.geometry.spatial2, True, opt.tick_length))

        error, next_frame = self.line_collision_check(next_frame, frame_buffer, current_spatial)
        error, end_frame = self.line_collision_check(end_frame, frame_buffer, next_frame.geometry.spatial2)

        return None, frame_buffer + [next_frame, end_frame]


    def line_collision_check(self, next_frame, frame_buffer, current_spatial):
        temporary_frames = []
        temporary_frames += frame_buffer
        for branch in self.branch_buffers:
            # Each branch is a list [branch_buffer, this_branch]
            temporary_frames += branch[0]
        collisions = self.tmap.collision_check(next_frame.geometry, temporary_frames, self.this_line)
        inters = []
        for collision in collisions:
            if collision.desc == 'text':
                return "big_error", next_frame
            else:
                interchange_spatial = Spatial(collision.intersection.x, collision.intersection.y, current_spatial.o)
                inters.append(InterchangeNode(interchange_spatial))
        next_frame.interchanges = inters
        return None, next_frame