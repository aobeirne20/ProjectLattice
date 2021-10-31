class Line():
    def __init__(self, origin_spatial, flip_spatial, trend, flip_trend, style_details):
        self.origin_spatial = origin_spatial
        self.flip_spatial = flip_spatial
        self.trend = trend
        self.flip_trend = flip_trend
        self.branches = []
        self.style_details = style_details

    def add_branch(self, frame_buffer):
        self.branches.append(Branch(frame_buffer))

    def form_origin_branch(self):
        pass

    def form_anti_branch(self):
        pass


class Branch():
    def __init__(self, frame_buffer):
        self.frame_buffer = frame_buffer
        self.segment_list = None
        self.station_list = None
        self.interchange_list = None