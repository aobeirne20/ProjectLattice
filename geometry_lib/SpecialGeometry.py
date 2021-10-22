from shapely.geometry import Point, LineString, LinearRing
import aggdraw
import numpy as np
from PIL import ImageDraw, ImageFont, Image

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.Geometry import Geometry

from parameters.StyleGuides import complete_style_guide as csg

o_to_anchor = {0: 'lm', 1: 'la', 2: 'ma', 3: 'ra', 4: 'rm', 5: 'rd', 6: 'md', 7: 'ld'}
o_to_align = {0: 'left', 1: 'left', 2: 'center', 3: 'right', 4: 'right', 5: 'right', 6: 'center', 7: 'left'}


class TextBBox(Geometry):
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

