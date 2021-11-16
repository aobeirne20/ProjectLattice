class Line():
    def __init__(self, style_details):
        self.origin_branch = None
        self.flip_branch = None
        self.sub_branch_starters = []
        self.branches = []

        self.style_details = style_details

    def set_origin_details(self, origin_spatial, flip_spatial, trend, flip_trend):
        self.origin_branch = Branch(origin_spatial, trend)
        self.flip_branch = Branch(flip_spatial, flip_trend)

    def give_origin_branch(self):
        return self.origin_branch

    def give_anti_branch(self):
        return self.flip_branch

    def form_sub_branch(self, spatial, trend):
        self.sub_branch_starters.append(Branch(spatial, trend))

    def unload_branch_buffer(self, branch_buffers):
        # This will append Nones to the lists, they are ignored by the renderer
        for buffer, branch in branch_buffers:
            for frame in buffer:
                branch.segment_list.append(frame.geometry)
                for station in frame.stations:
                    branch.station_list.append(station)
                for interchange in frame.interchanges:
                    branch.interchange_list.append(interchange)
                for sandwich in frame.sandwiches:
                    branch.sandwich_list.append(sandwich)
                for label in frame.labels:
                    branch.label_list.append(label)
            branch.frames = buffer
            self.branches.append(branch)

    # Not implemented yet
    def randomize_anti_trend(self):
        pass


class Branch():
    def __init__(self, origin_spatial, trend):
        self.origin_spatial = origin_spatial
        self.trend = trend

        # Data is stored redundantly, in both original frames and convenient lists. Consider changing later as needed
        self.segment_list, self.station_list, self.interchange_list, self.sandwich_list, self.label_list = [], [], [], [], []
        self.frames = None

