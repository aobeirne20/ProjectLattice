class Line():
    def __init__(self, origin_spatial, flip_spatial, trend, flip_trend):
        self.origin_spatial = origin_spatial
        self.flip_spatial = flip_spatial
        self.trend = trend
        self.flip_trend = flip_trend
        self.branches = []


class BranchBuffer():
    def __init__(self):
        self.path_buffer = []
        self.station_buffer = []
        self.interchange_buffer = []