from shapely.geometry import LinearRing, Point

from parameters.StyleGuides import complete_style_guide as csg


class TMap:
    def __init__(self, texterator):
        self.line_list = []
        self.interchange_list = []
        self.feature_list = []

        self.secant_not_picked_dir = [0, 1, 2, 3, 4, 5, 6, 7]
        self.secant_picked_dir = []
        self.logic_manifold = LinearRing([[0, 0], [csg.xs, 0], [csg.xs, csg.ys], [0, csg.ys]])
        self.texterator = texterator

    def collision_check(self, geometry, temporary_frames, this_line):
        collision_locs = []
        # Collision with the map lines
        for line in self.line_list:
            for branch in line.branches:
                for segment in branch.segment_list:
                    intersect = segment.logic_manifold.intersection(geometry.logic_manifold)
                    collision_locs = self.collision_check_processor(intersect, collision_locs, segment, line, "other_line")
        # Collision with the current buffers (this_branch and this_line)
        for frame in temporary_frames:
            if self.same_line_collision_preventer(frame, geometry):
                pass
            else:
                intersect = frame.geometry.logic_manifold.intersection(geometry.logic_manifold)
                collision_locs = self.collision_check_processor(intersect, collision_locs, frame.geometry, this_line, "same_line")

        # The River
        for feature in self.feature_list:
            if feature.feature_type_name == 'River':
                for label in feature.label_list:
                    intersect = label.logic_manifold.intersection(geometry.logic_manifold)
                    collision_locs = self.collision_check_processor(intersect, collision_locs, label, feature, "text")
                for segment in feature.render_list:
                    intersect = segment.logic_manifold.intersection(geometry.logic_manifold)
                    collision_locs = self.collision_check_processor(intersect, collision_locs, segment, feature, "river")

        # Labels
        for line in self.line_list:
            for branch in line.branches:
                for label in branch.label_list:
                    intersect = label.logic_manifold.intersection(geometry.logic_manifold)
                    collision_locs = self.collision_check_processor(intersect, collision_locs, label, line, "text")

        return collision_locs

    def collision_check_processor(self, intersect, collision_locs, segment, line, desc):
        if not intersect.is_empty:
            if intersect.geom_type == 'MultiPoint':
                intersect_list = []
                for point in intersect.geoms:
                    intersect_list.append(Collision(point, segment, line, desc))
                collision_locs += intersect_list
            elif intersect.geom_type == 'LineString':
                intersect_list = []
                for point in intersect.boundary.geoms:
                    intersect_list.append(Collision(point, segment, line, desc))
                collision_locs += intersect_list
            else:
                collision_locs += [Collision(intersect, segment, line, desc)]
        return collision_locs

    def same_line_collision_preventer(self, frame, geometry):
        return frame.geometry.spatial1.is_same_location(geometry.spatial1) or frame.geometry.spatial1.is_same_location(geometry.spatial2) or \
               frame.geometry.spatial2.is_same_location(geometry.spatial1) or frame.geometry.spatial2.is_same_location(geometry.spatial2)

    def distance_to_edge(self, geometry):
        return self.logic_manifold.distance(geometry.logic_manifold)

    def point_distance_to_edge(self, spatial):
        return self.logic_manifold.distance(Point([spatial.x, spatial.y]))

    def combine_interchanges(self):
        for line in self.line_list:
            for branch in line.branches:
                self.interchange_list += branch.interchange_list

    def parallel_check(self, geometry, temporary_frames, this_line):
        parallel_segments = []
        # Collision with the map lines
        for line in self.line_list:
            for branch in line.branches:
                for segment in branch.segment_list:
                    if self.paralell_orientation_check(segment.spatial1, segment.spatial2, geometry.spatial1, geometry.spatial2):
                        distance = segment.logic_manifold.distance(geometry.logic_manifold)
                        parallel_segments.append(Parallel(distance_to=distance, segment=segment, line=line))
        # Collision with the current buffers (this_branch and this_line)
        for frame in temporary_frames:
            if self.same_line_collision_preventer(frame, geometry):
                pass
            else:
                if self.paralell_orientation_check(frame.geometry.spatial1, frame.geometry.spatial2, geometry.spatial1, geometry.spatial2):
                    distance = frame.geometry.logic_manifold.distance(geometry.logic_manifold)
                    parallel_segments.append(Parallel(distance_to=distance, segment=frame, line=this_line))
        # The River
        for feature in self.feature_list:
            if feature.feature_type_name == 'River':
                for segment in feature.render_list:
                    if self.paralell_orientation_check(segment.spatial1, segment.spatial2, geometry.spatial1, geometry.spatial2):
                        distance = segment.logic_manifold.distance(geometry.logic_manifold)
                        parallel_segments.append(Parallel(distance_to=distance, segment=segment, line=feature))
        return parallel_segments

    def paralell_orientation_check(self, gspatial1, gspatial2, this_spatial1, this_spatial2):
        if gspatial1.o == this_spatial1.o and gspatial2.o and this_spatial2.o:
            return True
        elif gspatial1.o == this_spatial1.o + 4 and gspatial2.o == this_spatial2.o + 4:
            return True
        elif gspatial1.o == this_spatial2.o and gspatial2.o == this_spatial1.o:
            return True
        elif gspatial1.o == this_spatial2.o + 4 and gspatial2.o == this_spatial1.o + 4:
            return True
        else:
            return False

class Collision:
    def __init__(self, intersection, segment, line, desc):
        self.intersection = intersection
        self.segment = segment
        self.line = line
        self.desc = desc

    def __str__(self):
        return f"Collision with {self.desc}, {self.line} at {self.intersection}"


class Parallel:
    def __init__(self, distance_to, segment, line):
        self.distance_to = distance_to
        self.segment = segment
        self.line = line

    def __str__(self):
        return f"Distance to parallel segment {self.segment}, {self.line} is {self.distance_to}"

