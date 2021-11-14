from shapely.geometry import LinearRing, Point

from parameters.StyleGuides import complete_style_guide as csg


class TMap:
    def __init__(self):
        self.line_list = []
        self.interchange_list = []
        self.feature_list = []

        self.secant_not_picked_dir = [0, 1, 2, 3, 4, 5, 6, 7]
        self.secant_picked_dir = []
        self.logic_manifold = LinearRing([[0, 0], [csg.xs, 0], [csg.xs, csg.ys], [0, csg.ys]])

    def collision_check(self, geometry, temporary_frames):
        collision_locs = []
        # Collision with the map
        for line in self.line_list:
            for branch in line.branches:
                for segment in branch.segment_list:
                    intersect = segment.logic_manifold.intersection(geometry.logic_manifold)
                    collision_locs = self.collision_check_processor(intersect, collision_locs)
        # Collision with the current buffers (this_branch and this_line)
        for frame in temporary_frames:
            if self.same_line_collision_preventer(frame, geometry):
                pass
            else:
                intersect = frame.geometry.logic_manifold.intersection(geometry.logic_manifold)
                collision_locs = self.collision_check_processor(intersect, collision_locs)

        return collision_locs

    def collision_check_processor(self, intersect, collision_locs):
        if not intersect.is_empty:
            if intersect.geom_type == 'MultiPoint':
                intersect_list = []
                for point in intersect:
                    intersect_list.append(point)
                collision_locs += intersect_list
            elif intersect.geom_type == 'LineString':
                intersect_list = []
                for point in intersect.boundary:
                    intersect_list.append(point)
                collision_locs += intersect_list
            else:
                collision_locs += [intersect]
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

