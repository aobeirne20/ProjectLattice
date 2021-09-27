import random

from MiscRenderers import RM1_LondonRiver, RM2_LondonStations, RM3_LondonTextPreparer, RM4_LondonTextRenderer
from LineRenderers import LR1_LondonNormal

import style_data
import PIL
import numpy as np
from PIL import Image, ImageOps


class R1_London:
    def __init__(self, art_style, size_tp, net_map):
        self.art_style = art_style
        self.art_type = self.art_style
        self.SD = style_data.StyleDatabase
        self.xs = size_tp[0]
        self.ys = size_tp[1]
        self.map = net_map
        self.render_slices = []
        self.text_slice = None
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
            rm = LR1_LondonNormal.LR1_LondonNormal(self.xs, self.ys, line, self.art_style)
            render_slice, station_loc_list = rm.render()
            self.render_slices.append(render_slice)
            self.loc_needing_text += station_loc_list
        if self.art_type['name'] == 'Brightline' or self.art_type['name'] == 'Anti-brightline' or self.art_type['name'] == 'Darkline' or self.art_type['name'] == 'Anti-darkline':
            num_bright = np.random.choice([1])
            slices_to_color = []
            for n in range(0, num_bright):
                slices_to_color.append(random.randint(0, len(self.render_slices)-1))

            for n in range(0, len(self.render_slices)):
                if slices_to_color.count(n) > 0:
                    pass
                else:
                    self.render_slices[n] = PIL.ImageOps.grayscale(self.render_slices[n])

    def render_loci(self):
        rm = RM2_LondonStations.RM2_LondonStations(self.xs, self.ys, self.map.locus_list, self.map.line_list)
        render_slice = rm.render()
        self.render_slices = self.render_slices + render_slice

    def render_text(self):
        self.loc_needing_text = self.map.text_list
        if self.art_style['background'] == 'darkblue' or self.art_style['background'] == 'black':
            text_color = (255, 255, 255, 255)
        else:
            text_color = (0, 0, 0, 255)
        text_giver = RM3_LondonTextPreparer.RM3_LondonTextPreparer()
        rm = RM4_LondonTextRenderer.RM4_LondonTextRenderer(self.loc_needing_text, self.xs, self.ys, text_giver, text_color)
        self.text_slice = rm.render()

    def give_render(self):
        for r_slice in self.render_slices:
            self.slice_collector.paste(r_slice, mask=r_slice)
        return self.slice_collector, self.text_slice







    def invert_w_transperancy_colora(self, img):
        r, g, b, a = img.split()
        def invert(image):
            return image.point(lambda p: 255 - p)
        r, g, b = map(invert, (r, g, b))
        img2 = Image.merge(img.mode, (r, g, b, a))
        return img2