from shapely.geometry import Point, LineString, LinearRing
import aggdraw
import numpy as np
from PIL import ImageDraw, ImageFont, Image

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.Geometry import Geometry

from parameters.StyleGuides import complete_style_guide as csg


class TextBBox(Geometry):
    def __init__(self, spatial_station: Spatial, text: str, offset: int, font: str, font_size: int):
        super().__init__()
        self.spatial_station = spatial_station
        self.spatial_anchor = Spatial(x=spatial_station.x + spatial_station.o.vx(offset),
                                      y=spatial_station.y + spatial_station.o.vy(offset),
                                      o=spatial_station.o)

        o_to_anchor = {0: 'lm', 1: 'lt', 2: 'mt', 3: 'rt', 4: 'rm', 5: 'rb', 6: 'mb', 7: 'lb'}
        o_to_align = {0: 'left', 1: 'left', 2: 'center', 3: 'right', 4: 'right', 5: 'right', 6: 'center', 7: 'left'}
        anchor = o_to_anchor[spatial_station.o]
        align = o_to_align[spatial_station.o]

        psuedo_img = Image.new('RGBA', (500, 500), color=(0, 0, 0, 0))
        psuedo_draw = ImageDraw.Draw(psuedo_img)

        fonto = ImageFont.truetype("ITC - JohnstonITCPro-Medium.otf", font_size)
        bbox = psuedo_draw.multiline_textbbox(self.spatial_anchor.t, text, font=fonto, anchor=anchor, align=align)
        print(bbox)

        #self.logic_manifold =

    def execute_render(self, draw: ImageDraw.Draw):
        draw.multiline_text()


class RailLogo(Geometry):
    pass



x = TextBBox(Spatial(x=10, y=10, o=degree(0)), "tester", 5, "fonts/ITC - JohnstonITCPro-Medium.otf", 10)