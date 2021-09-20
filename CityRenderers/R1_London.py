from MiscRenderers import RM1_LondonRiver

import style_data
import PIL
from PIL import Image, ImageOps


class R1_London:
    def __init__(self, art_type, size_tp, net_map):
        self.art_type = art_type
        self.SD = style_data.StyleDatabase
        self.xs = size_tp[0]
        self.ys = size_tp[1]
        self.map = net_map
        self.render_slices = []
        self.slice_collector = PIL.Image.new('RGBA', size_tp, (0, 0, 0, 0))

        self.render_primary_features()

    def render_primary_features(self):
        for feature in self.map.primary_feature_list:
            if feature.name == "LondonRiver":
                rm = RM1_LondonRiver.RM1_LondonRiver(self.xs, self.ys, feature.render_list)
                self.render_slices.append(rm.render())

    def give_render(self):
        for r_slice in self.render_slices:
            self.slice_collector.paste(r_slice, mask=r_slice)
        return self.slice_collector







