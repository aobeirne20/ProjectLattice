class Line():
    def __init__(self, origin_spatial, flip_spatial, trend, flip_trend, style_details):
        self.origin_spatial = origin_spatial
        self.flip_spatial = flip_spatial
        self.trend = trend
        self.flip_trend = flip_trend
        self.branches = []
        self.style_details = style_details

    def add_branch(self, segment_list, station_list, interchange_list):
        self.branches.append(Branch(segment_list, station_list, interchange_list))


class Branch():
    def __init__(self, segment_list, station_list, interchange_list):
        self.segment_list = segment_list
        self.station_list = station_list
        self.interchange_list = interchange_list