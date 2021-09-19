from Maps import M1_London

from MiscRenderers import RM1_LondonRiver

import style_data


class R1_London:
    def __init__(self, art_type, size_tp, mapp):
        self.art_type = art_type
        self.SD = style_data.StyleDatabase
        self.xs = size_tp[0]
        self.ys = size_tp[1]
        self.x_scale = (int(size_tp[0] / self.SD.map_style_guide["London"]["grid_scale"]))
        self.y_scale = (int(size_tp[1] / self.SD.map_style_guide["London"]["grid_scale"]))
        self.scale_multi = self.xs/self.x_scale
        if self.scale_multi != self.ys/self.y_scale:
            raise SystemExit("X and Y Scaling not uniform!")
        self.map = mapp
        self.render_slices = []

        self.render_primary_features()


    def render_primary_features(self):
        for feature in self.map.primary_feature_list:
            if feature["name"] == "LondonRiver":
                rm = RM1_LondonRiver.RM1_LondonRiver(self.xs, self.ys,
                                                     self.scale_multi, feature["render_path"])
                self.render_slices.append(rm.render())





