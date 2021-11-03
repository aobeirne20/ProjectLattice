class Line():
    def __init__(self, origin_spatial, flip_spatial, trend, flip_trend, style_details):
        self.origin_branch = Branch(origin_spatial, trend)
        self.flip_branch = Branch(flip_spatial, flip_trend)

        self.sub_branches = []
        self.branches = []
        self.buffers = []
        self.style_details = style_details

    def pin_branch(self, branch):
        self.buffers.append(branch)

    def form_origin_branch(self):
        return self.origin_branch

    def form_anti_branch(self):
        return self.flip_branch

    def form_sub_branch(self, spatial, trend):
        self.sub_branches.append(Branch(spatial, trend))

    def unload_buffers(self):
        for buffer in self.buffers:
            segment_list = []
            station_list = []
            interchange_list = []
            sandwich_list = []
            for frame in buffer.frame_buffer:
                segment_list.append(frame.geometry)
                for station in frame.stations:
                    station_list.append(station)
                for interchange in frame.interchanges:
                    interchange_list.append(interchange)
                for sandwich in frame.sandwiches:
                    sandwich_list.append(sandwich)
            buffer.segment_list, buffer.station_list, buffer.interchange_list, buffer.sandwich_list = segment_list, station_list, interchange_list, sandwich_list
            self.branches.append(buffer)


    def randomize_anti_trend(self):
        pass


class Branch():
    def __init__(self, origin_spatial, trend):
        self.origin_spatial = origin_spatial
        self.trend = trend
        self.frame_buffer, self.segment_list, self.station_list, self.interchange_list, self.sandwich_list = None, None, None, None, None

    def pin_buffer(self, frame_buffer):
        self.frame_buffer = frame_buffer
        # Others currently unused
