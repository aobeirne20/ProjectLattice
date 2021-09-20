import numpy as np

class Map:
    def __init__(self, xs, ys):
        self.size = (xs, ys)
        self.primary_feature_list = []
        self.line_list = []
        self.locus_list = []
        self.secondary_feature_list = []


class Line:
    def __init__(self, name, color, style, render_list):
        self.name = name
        self.color = color
        self.style = style
        self.loc_list = render_list


class Locus:
    def __init__(self, style, loc):
        self.style = style
        self.loc = loc





