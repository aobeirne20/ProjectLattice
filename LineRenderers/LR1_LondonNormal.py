import geometric_elements as ge
import aggdraw

import PIL
from PIL import Image
import style_data as sd


class LR1_LondonNormal:
    def __init__(self, xs, ys, render_path, style):
        self.xs = xs
        self.ys = ys
        self.render_path = render_path
        self.style = style

    def render(self):
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
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
        return img_slice