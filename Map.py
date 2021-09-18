
class Map:
    def __init__(self):
        self.origin_vertex = None
        self.line_list = []
        self.locus_list = []
        self.feature_list = []

    def add_line(self, color, style, loc_list):
        self.line_list.append(Line(color, style, loc_list))

    def add_feature(self, name, loc_list):
        self.feature_list.append(Feature(name, loc_list))


class Line:
    def __init__(self, color, style, loc_list):
        self.color = color
        self.style = style
        self.loc_list = loc_list


class Locus:
    def __init__(self, style, loc):
        self.style = style
        self.loc = loc


class Feature:
    def __init__(self, name, loc_list):
        self.name = name
        self.loc_list = loc_list
