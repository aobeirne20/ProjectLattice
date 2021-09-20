import geometric_elements as ge
import aggdraw

import PIL
from PIL import Image


class RM1_LondonRiver:
    def __init__(self, xs, ys, render_path):
        self.xs = xs
        self.ys = ys
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


