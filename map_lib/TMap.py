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

    def collision_check(self, geometry, buffer, line):
        collision_locs = []
        # Collision with the map
        for line in self.line_list:
            for branch in line.branches:
                for segment in branch.segment_list:
                    intersect = segment.logic_manifold.intersection(geometry.logic_manifold)
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

        # # Collision with the current buffer
        # for frame in buffer:
        #     intersect = frame.geometry.logic_manifold.intersection(geometry.logic_manifold)
        #     if not intersect.is_empty:
        #         if frame.geometry.spatial1 != geometry.spatial1 and frame.geometry.spatial1 != geometry.spatial2 and \
        #                 frame.geometry.spatial2 != geometry.spatial1 and frame.geometry.spatial2 != geometry.spatial2:
        #             if intersect.geom_type == 'MultiPoint':
        #                 intersect_list = []
        #                 for point in intersect:
        #                     intersect_list.append(point)
        #                 collision_locs += intersect_list
        #             else:
        #                 collision_locs += [intersect]
        #
        # # Collision with the current line THIS NEEDS TO BE FIXED
        # for buffer in line.buffers:
        #     for frame in buffer.frame_buffer:
        #         intersect = frame.geometry.logic_manifold.intersection(geometry.logic_manifold)
        #         if not intersect.is_empty:
        #             if intersect.geom_type == 'MultiPoint':
        #                 intersect_list = []
        #                 for point in intersect:
        #                     intersect_list.append(point)
        #                 collision_locs += intersect_list
        #             else:
        #                 collision_locs += [intersect]


        return collision_locs

    def distance_to_edge(self, geometry):
        return self.logic_manifold.distance(geometry.logic_manifold)

    def point_distance_to_edge(self, spatial):
        return self.logic_manifold.distance(Point([spatial.x, spatial.y]))

    def combine_interchanges(self):
        for line in self.line_list:
            for branch in line.branches:
                self.interchange_list += branch.interchange_list

