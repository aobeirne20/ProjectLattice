import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.StationGeometry import Station, Terminus
from geometry_lib.InterchangeGeometry import InterchangeNode, InterchangeConnector, DarkNode
from geometry_lib.TrackGeometry import Straight, Arc
from map_lib.Line import Line
from London.generate_lib.line import gLineSecantHelpers, ErrorWrapper

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


class gLineSecant():
    def __init__(self, tmap, line_details):
        self.tmap = tmap
        self.this_line = Line(line_details)
        self.this_branch = None
        self.sub_branches = []
        self.branch_buffers = []

        # ORIGIN BRANCH
        overall_error = ErrorWrapper.Error(error_desc='placeholder')
        while overall_error is not None:
            self.this_line.set_origin_details(*gLineSecantHelpers.gen_origin(tmap))
            self.this_branch, origin_frame_buffer = self.this_line.give_origin_branch(), []
            origin_branch = self.this_branch
            overall_error, origin_frame_buffer, _ = self.r_frame_straight(origin_frame_buffer)

            # ANTI ORIGIN BRANCH
            if overall_error is None:
                overall_error = ErrorWrapper.Error(error_desc='placeholder')
                attempts = 5
                while attempts > 0:
                    self.this_branch, anti_origin_frame_buffer = self.this_line.give_anti_branch(), []
                    anti_origin_branch = self.this_branch
                    overall_error, anti_origin_frame_buffer, _ = self.r_frame_curve(anti_origin_frame_buffer)
                    if overall_error is None:
                        self.save_this_branch_buffer(origin_frame_buffer, origin_branch)
                        self.save_this_branch_buffer(anti_origin_frame_buffer, anti_origin_branch)
                        break
                    else:
                        attempts -= 1

        # SUB-BRANCHES
        for branch in self.this_line.sub_branch_starters:
            self.this_branch, frame_buffer = branch, []
            error, frame_buffer = self.r_frame_straight(frame_buffer)
            if error is None:
                self.save_this_branch_buffer(frame_buffer, self.this_branch)

    def return_line(self):
        if int(self.this_line.origin_branch.trend) in self.tmap.secant_not_picked_dir:
            self.tmap.secant_not_picked_dir.remove(int(self.this_line.origin_branch.trend))
            self.tmap.secant_picked_dir.append(int(self.this_line.origin_branch.trend))

        used_names = []
        for branch in self.branch_buffers:
            for frame in branch[0]:
                if frame.labels:
                    for label in frame.labels:
                        used_names.append(label.render_manifold.text)
        self.tmap.texterator.finalize_removal(actual_used_names=used_names, pool=self.this_line.style_details['station_type'])

        self.this_line.unload_branch_buffer(self.branch_buffers)
        return self.this_line

    def save_this_branch_buffer(self, frame_buffer, branch):
        self.branch_buffers.append([frame_buffer, branch])

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # STRAIGHT SEGMENTS
    def r_frame_straight(self, frame_buffer):
        terminus_counter = 0
        while True:
            current_spatial = self.this_branch.origin_spatial if not frame_buffer else frame_buffer[-1].geometry.spatial2
            next_frame = gLineSecantHelpers.BufferFrame(Straight(current_spatial, gLineSecantHelpers.length_normal_dist()))

            error, next_frame = self.line_collision_check(next_frame, frame_buffer)
            if error is not None:
                return "text_error", next_frame, -1
            error = self.line_parallel_check(next_frame, frame_buffer)
            if error is not None:
                return "text_error", next_frame, -1

            if self.tmap.distance_to_edge(next_frame.geometry) <= opt.map_border_buffer:
                if terminus_counter > 2:
                    terminus_counter += 1
                    continue
                else:
                    error, frame_buffer, _ = self.r_terminus(frame_buffer)
                    return None, frame_buffer, 0

            next_frame = gLineSecantHelpers.gen_stations(next_frame, self.tmap.texterator, self.this_line.style_details['station_type'])

            error, satisified_frame_buffer, mover = self.r_frame_curve(frame_buffer + [next_frame])
            if error is None:
                return None, satisified_frame_buffer, 0
            elif mover == 0:
                continue
            else:
                return error, frame_buffer, mover+1

        return "big_error", frame_buffer, 0

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # CURVE SEGMENTS
    def r_frame_curve(self, frame_buffer):
        terminus_counter = 0
        while True:
            current_spatial = self.this_branch.origin_spatial if not frame_buffer else frame_buffer[-1].geometry.spatial2
            next_frame = gLineSecantHelpers.BufferFrame(Arc(current_spatial, gLineSecantHelpers.curve_change_choice(self.this_branch.trend, current_spatial), opt.cr_line))

            error, next_frame = self.line_collision_check(next_frame, frame_buffer)
            if error is not None:
                return "text_error", next_frame, -1

            if self.tmap.distance_to_edge(next_frame.geometry) <= opt.map_border_buffer:
                if terminus_counter > 2:
                    terminus_counter += 1
                    continue
                else:
                    error, frame_buffer, _ = self.r_terminus(frame_buffer)
                    return None, frame_buffer, 0

            error, satisified_frame_buffer, mover = self.r_frame_straight(frame_buffer + [next_frame])
            if error is None:
                return None, satisified_frame_buffer, 0
            elif mover == 0:
                continue
            else:
                return error, frame_buffer, mover+1

        return "big_error", frame_buffer

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # TERMINUS SEGMENTS
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

        error, next_frame = self.line_collision_check(next_frame, frame_buffer)
        error, end_frame = self.line_collision_check(end_frame, frame_buffer)

        next_frame = gLineSecantHelpers.gen_stations(next_frame, self.tmap.texterator, self.this_line.style_details['station_type'])

        return None, frame_buffer + [next_frame, end_frame], 0



    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def line_collision_check(self, next_frame, frame_buffer):
        temporary_frames = []
        temporary_frames += frame_buffer
        for branch in self.branch_buffers:
            # Each branch is a list [branch_buffer, this_branch]
            temporary_frames += branch[0]
        collisions = self.tmap.collision_check(next_frame.geometry, temporary_frames, self.this_line)
        inters = []
        for collision in collisions:
            if collision.desc == 'text':
                return "text_collision", next_frame
            if collision.desc == 'river':
                continue
            interchange_spatial = Spatial(collision.intersection.x, collision.intersection.y, next_frame.geometry.spatial1.o)
            inters.append(InterchangeNode(interchange_spatial))
        next_frame.interchanges = inters
        return None, next_frame

    def line_parallel_check(self, next_frame, frame_buffer):
        temporary_frames = []
        temporary_frames += frame_buffer
        for branch in self.branch_buffers:
            # Each branch is a list [branch_buffer, this_branch]
            temporary_frames += branch[0]
        parallels = self.tmap.parallel_check(next_frame.geometry, temporary_frames, self.this_line)
        for parallel in parallels:
            if parallel.distance_to < opt.parallel_min_distance:
                return "too_close"
        return None



