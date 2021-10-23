from shapely.geometry import box
import aggdraw
import numpy as np
from PIL import ImageDraw, ImageFont, Image

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.Geometry import Geometry

from parameters.StyleGuides import complete_style_guide as csg

o_to_anchor = {0: 'lm', 1: 'la', 2: 'ma', 3: 'ra', 4: 'rm', 5: 'rd', 6: 'md', 7: 'ld'}
o_to_align = {0: 'left', 1: 'left', 2: 'center', 3: 'right', 4: 'right', 5: 'right', 6: 'center', 7: 'left'}


class TextBox(Geometry):
    def __init__(self, spatial_station: Spatial, text: str, offset: int, font_name: str, font_size: int):
        super().__init__()
        self.spatial_station = spatial_station
        self.spatial_anchor = Spatial(x=spatial_station.x + spatial_station.o.vx(offset),
                                      y=spatial_station.y + spatial_station.o.vy(offset),
                                      o=spatial_station.o)

        anchor = o_to_anchor[spatial_station.o]
        align = o_to_align[spatial_station.o]

        font = ImageFont.truetype(font=font_name, size=font_size)
        pseudo_draw = ImageDraw.Draw(Image.new('RGBA', (csg.xs, csg.ys), color=(0, 0, 0, 0)))
        bbox = pseudo_draw.multiline_textbbox(self.spatial_anchor.t, text, font=font, anchor=anchor, align=align)

        if self.spatial_anchor.o == 0 or self.spatial_anchor.o == 4:
            y_new_center = np.average([bbox[1], bbox[3]])
            y_adjustment = self.spatial_anchor.y - y_new_center
            self.spatial_anchor = Spatial(x=self.spatial_anchor.x, y=self.spatial_anchor.y + y_adjustment, o=self.spatial_anchor.o)

        self.logic_manifold = box(minx=min(bbox[0], bbox[2]), miny=min(bbox[1], bbox[3]), maxx=max(bbox[0], bbox[2]), maxy=max(bbox[1], bbox[3]))

        self.render_manifold = TextRenderManifold(text=text, xy=self.spatial_anchor.t, font=font, anchor=anchor, align=align)

    def execute_render(self, draw: ImageDraw.Draw, color):
        rm = self.render_manifold
        draw.multiline_text(xy=rm.xy, text=rm.text, font=rm.font, fill=color, anchor=rm.anchor, align=rm.align)


class RailLogo(Geometry):
    pass


class TextRenderManifold():
    def __init__(self, text, xy, font, anchor, align):
        self.text = text
        self.font = font
        self.xy = xy
        self.anchor = anchor
        self.align = align

