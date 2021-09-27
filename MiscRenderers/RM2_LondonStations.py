import geometric_elements as ge
import aggdraw
import math

import PIL
from PIL import Image
import style_data as sd

class RM2_LondonStations:
    def __init__(self, xs, ys, locus_list, line_list):
        self.xs = xs
        self.ys = ys
        self.locus_list = locus_list
        self.line_list = line_list
        self.station_slices = []

    def render(self):
        for type_of_locus in ['Interchange']:
            if type_of_locus == 'Interchange':
                img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
                draw = aggdraw.Draw(img_slice)
                pen = aggdraw.Pen(color=(0, 0, 0, 255), width=7*sd.StyleDatabase.t_scale)
                brush = aggdraw.Brush(color=(255, 255, 255, 255))
                for locus in self.locus_list:
                    if locus['name'] == 'Interchange':
                        bounds = (locus['location'][0] + 17*sd.StyleDatabase.t_scale, locus['location'][1] + 17*sd.StyleDatabase.t_scale,
                                  locus['location'][0] - 17*sd.StyleDatabase.t_scale, locus['location'][1] - 17*sd.StyleDatabase.t_scale)
                        draw.ellipse(bounds, pen, brush)
                draw.flush()
                self.station_slices.append(img_slice)

        return self.station_slices

