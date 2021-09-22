import numpy as np
import math

import MapChecks as MC


class Map:
    def __init__(self, xs, ys, scale):
        self.size = (xs, ys)
        self.scale = scale
        self.primary_feature_list = []
        self.line_list = []
        self.locus_list = []
        self.secondary_feature_list = []

    # Returns the distance of the given location to its closest object, and the name of that object
    def node_check(self, loc):
        closest_d = np.maximum(self.size[0], self.size[1])
        for thing in self.primary_feature_list + self.line_list:
            if isinstance(thing, Line):
                for seg in thing.render_list:
                    dis = MC.distance_between_point_and_seg(seg, loc)
                    if dis < closest_d:
                        thing_name = thing.name
                        closest_d = dis
        return {"distance": closest_d, "object": thing_name}

    # Returns the distance of the given segment to its closest parallel object, and the name of that object
    def seg_parallel_check(self, seg2):
        thing_name = None
        closest_d = np.maximum(self.size[0], self.size[1])
        for thing in self.primary_feature_list + self.line_list:
            if isinstance(thing, Line):
                for seg1 in thing.render_list:
                    dis = MC.parallel_distance_between_seg_and_seg(seg1, seg2)
                    if dis < closest_d:
                        thing_name = thing.name
                        closest_d = dis
        return {"distance": closest_d, "object": thing_name}

    # Returns the location and object of any crossings
    def seg_crossing_check(self, seg2):
        crossing_dict = []
        for thing in self.primary_feature_list + self.line_list:
            if isinstance(thing, Line):
                for seg1 in thing.render_list:
                    cross_loc = MC.location_of_intersection_of_two_segs(seg1, seg2)
                    if cross_loc is not None:
                        crossing_dict.append({"location": cross_loc, "object": thing.name, "geometry": type(seg1).__name__})
        return crossing_dict

    def interchange_dist_check(self, locx, locy):
        closest_d = np.maximum(self.size[0], self.size[1])
        for thing in self.locus_list:
            x1 = thing["location"][0]
            y1 = thing["location"][1]
            dis = np.linalg.norm(np.asarray([x1, y1])-np.asarray([locx, locy]))
            if dis < closest_d:
                closest_d = dis
        return closest_d



    # Node checks the new (next) node, for potential sandwich section segments
    def seg_node_check(self, seg2):
        return self.node_check(seg2.loc2)


class Line:
    def __init__(self, name, style, render_list):
        self.name = name
        self.style = style
        self.render_list = render_list


class Locus:
    def __init__(self, style, loc):
        self.style = style
        self.loc = loc





