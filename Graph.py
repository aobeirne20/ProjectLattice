
class Graph:
    def __init__(self):
        self.origin_vertex = None
        self.vertex_list = []
        self.edge_list = []
        self.feature_list = []

    def add_edge(self, color, loc1, loc2):
        self.edge_list.append(Edge(color, loc1, loc2))


class Vertex:
    def __init__(self, rtype, loc):
        self.rtype = rtype
        self.loc = loc


class Edge:
    def __init__(self, color, loc1, loc2):
        self.color = color
        self.loc1 = loc1
        self.loc2 = loc2


class Feature:
    def __init__(self):
        pass
