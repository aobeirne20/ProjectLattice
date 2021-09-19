import geometric_elements as ge
import aggdraw

import PIL
from PIL import Image


class RM1_LondonRiver:
    def __init__(self, xs, ys, s_m, render_path):
        self.xs = xs
        self.ys = ys
        self.s_m = s_m
        self.render_path = render_path

    def render(self):
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
        # Custom River Pen
        pens = [aggdraw.Pen((0, 180, 241, 255), 80), aggdraw.Pen((199, 234, 252, 255), 60)]
        draw = aggdraw.Draw(img_slice)
        draw.setantialias(False)

        for pen in pens:
            for seg in self.render_path:
                if isinstance(seg, ge.Arc90):
                    seg.render_specific(pen, draw, self.s_m)
                    pass
            for seg in self.render_path:
                if isinstance(seg, ge.Arc45):
                    seg.render_specific(pen, draw, self.s_m)
                    pass
            for seg in self.render_path:
                if isinstance(seg, ge.Segment):
                    seg.render_specific(pen, draw, self.s_m)

        draw.flush()
        return img_slice.resize((6000, 4000), PIL.Image.ANTIALIAS)


