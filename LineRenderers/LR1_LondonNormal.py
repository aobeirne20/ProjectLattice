import geometric_elements as ge
import aggdraw
import math

import PIL
from PIL import Image
import style_data as sd

from MiscRenderers import RM3_LondonTextPreparer

straight_unit_vectors = {0: (1, 0), 45: (math.sqrt(0.5), -1 * math.sqrt(0.5)), 90: (0, -1), 135: (-1 * math.sqrt(0.5), -1 * math.sqrt(0.5)),
                         180: (-1, 0), 225: (-1 * math.sqrt(0.5), math.sqrt(0.5)), 270: (0, 1), 315: (math.sqrt(0.5), math.sqrt(0.5)), 360: (1, 0)}

class LR1_LondonNormal:
    def __init__(self, xs, ys, line):
        self.xs = xs
        self.ys = ys
        self.render_path = line.render_list
        self.station_list = line.station_list

        self.style = line.style

    def render(self):
        station_text_location_list = []
        # STATION NOTCH RENDERING
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
        draw = aggdraw.Draw(img_slice)
        black_border_pen = aggdraw.Pen(color=(0, 0, 0, 255), width=7 * sd.StyleDatabase.t_scale)
        white_fill_brush = aggdraw.Brush(color=(255, 255, 255, 255))
        single_color_pen = aggdraw.Pen(self.style["color"], 11 * sd.StyleDatabase.t_scale)
        for station in self.station_list:
            if station['name'] == 'Railway':
                bounds = (station['location'][0] + 17 * sd.StyleDatabase.t_scale, station['location'][1] + 17 * sd.StyleDatabase.t_scale,
                          station['location'][0] - 17 * sd.StyleDatabase.t_scale, station['location'][1] - 17 * sd.StyleDatabase.t_scale)
                station_text_location_list.append({'location': station['location'], 'type': self.style['type']})
                draw.ellipse(bounds, black_border_pen, white_fill_brush)
            elif station['name'] == 'Single':
                pos1 = station['location']
                vector_along = (
                    19 * sd.StyleDatabase.t_scale * straight_unit_vectors[station['orientation']][0],
                    19 * sd.StyleDatabase.t_scale * straight_unit_vectors[station['orientation']][1])
                pos2 = (pos1[0] + vector_along[0], pos1[1] + vector_along[1])
                draw.line((pos1[0], pos1[1],
                           pos2[0], pos2[1]), single_color_pen)
                station_text_location_list.append({'location': pos2, 'type': self.style['type']})
        draw.flush()


        # LINE RENDERING
        if self.style["style"] == "double":
            pens = [aggdraw.Pen(self.style["color"], 18*sd.StyleDatabase.t_scale),
                    aggdraw.Pen((255, 255, 255, 255), 8*sd.StyleDatabase.t_scale)]
        if self.style["style"] == "single":
            pens = [aggdraw.Pen(self.style["color"], 18*sd.StyleDatabase.t_scale)]
        draw = aggdraw.Draw(img_slice)
        draw.setantialias(False)

        for pen in pens:
            for seg in self.render_path:
                if isinstance(seg, ge.Arc90):
                    seg.render(pen, draw)
                    pass
            for seg in self.render_path:
                if isinstance(seg, ge.Arc45):
                    seg.render(pen, draw)
                    pass
            for seg in self.render_path:
                if isinstance(seg, ge.Segment):
                    seg.render(pen, draw)

        draw.flush()
        return img_slice, station_text_location_list