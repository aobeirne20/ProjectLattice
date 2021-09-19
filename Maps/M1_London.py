import numpy as np

class Map:
    def __init__(self, xgs, ygs):
        self.origin_vertex = None
        self.line_list = []
        self.locus_list = []
        self.primary_feature_list = []
        self.secondary_feature_list = []
        self.collision_array = np.empty((ygs, xgs), dtype=object)

    def add_line(self, color, style, loc_list):
        self.line_list.append(Line(color, style, loc_list))


class Line:
    def __init__(self, color, style, loc_list):
        self.color = color
        self.style = style
        self.loc_list = loc_list


class Locus:
    def __init__(self, style, loc):
        self.style = style
        self.loc = loc


class River:
    def __init__(self, renderer_name, loc_list):
        self.renderer_name = renderer_name
        self.loc_list = loc_list


class IntersectNode:
    __slots__ = ['name', 'orientation']
    def __init__(self, name, orientation):
        self.name = name
        self.orientation = orientation
