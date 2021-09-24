from MiscRenderers import RM1_LondonRiver, RM2_LondonStations, RM3_LondonTextPreparer, RM4_LondonTextRenderer
from LineRenderers import LR1_LondonNormal

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
        self.loc_needing_text = []
        self.slice_collector = PIL.Image.new('RGBA', size_tp, (0, 0, 0, 0))

        self.render_primary_features()
        self.render_lines()
        self.render_loci()
        self.render_text()

    def render_primary_features(self):
        for feature in self.map.primary_feature_list:
            if feature.name == "LondonRiver":
                rm = RM1_LondonRiver.RM1_LondonRiver(self.xs, self.ys, feature.render_list)
                self.render_slices.append(rm.render())

    def render_lines(self):
        for line in self.map.line_list:
            rm = LR1_LondonNormal.LR1_LondonNormal(self.xs, self.ys, line)
            render_slice, station_loc_list = rm.render()
            self.render_slices.append(render_slice)
            self.loc_needing_text += station_loc_list

    def render_loci(self):
        rm = RM2_LondonStations.RM2_LondonStations(self.xs, self.ys, self.map.locus_list, self.map.line_list)
        render_slice, station_loc_list = rm.render()
        self.render_slices = self.render_slices + render_slice
        self.loc_needing_text += station_loc_list

    def render_text(self):
        text_giver = RM3_LondonTextPreparer.RM3_LondonTextPreparer()
        rm = RM4_LondonTextRenderer.RM4_LondonTextRenderer(self.loc_needing_text, self.xs, self.ys, text_giver)
        self.render_slices.append(rm.render())

    def give_render(self):
        for r_slice in self.render_slices:
            self.slice_collector.paste(r_slice, mask=r_slice)
        return self.slice_collector







