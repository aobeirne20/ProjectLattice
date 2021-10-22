from geometry_lib.SpecialGeometry import TextBBox
from geometry_lib.degree import degree
from geometry_lib.Spatial import Spatial
from PIL import ImageDraw, Image
from parameters.StyleGuides import complete_style_guide as csg

from geometry_lib.degree import degree
from geometry_lib.TrackGeometry import Straight, Arc
from geometry_lib.StationGeometry import Station, Terminus
from geometry_lib.InterchangeGeometry import InterchangeNode, InterchangeConnector, HandicapNode

from geometry_lib.Spatial import Spatial

import aggdraw
import PIL

import aggdraw



s1 = Spatial(x=200, y=200, o=degree(0))
a = Straight(s1, 100)
b = Arc(a.spatial2, -3, 50)
c = Arc(b.spatial2, 1, 100)
d = Station(a.spatial2, False, 30)
e = Terminus(c.spatial2, False, 30)
f = InterchangeNode(b.spatial2)
h = HandicapNode(a.spatial1)
i = InterchangeConnector(b.spatial2, a.spatial1)
pen = aggdraw.Pen((255, 255, 255, 255), 20)
brush = aggdraw.Brush((0, 0, 0, 255))
brush2 = aggdraw.Brush((255, 255, 255, 255))
pen2 = aggdraw.Pen((0, 0, 0, 255), 20)
pen3 = aggdraw.Pen((255, 255, 255, 255), 10)
bluebrush = aggdraw.Brush((28, 63, 149, 255))
bluepen = aggdraw.Pen((28, 63, 149, 255), 4)
wpen = aggdraw.Pen((255, 255, 255, 255), 2.5)


x = TextBBox(d.spatial_station, "St James's\nPark", 5, "fonts/ITC - JohnstonITCPro-Medium.otf", 20)










img_slice = PIL.Image.new('RGBA', (500, 500), color=(200, 80, 100, 255))
draw = aggdraw.Draw(img_slice)
a.execute_render(draw, pen)
b.execute_render(draw, pen)
c.execute_render(draw, pen)
d.execute_render(draw, pen)
e.execute_render(draw, pen)
f.execute_render(draw, brush, 20)
i.execute_render(draw, pen2)
f.execute_render(draw, brush2, 15)
i.execute_render(draw, pen3)
h.execute_render(draw, bluebrush, 16, bluepen, wpen)
draw.flush()

draw2 = ImageDraw.Draw(img_slice)
x.execute_render(draw2, csg.palette_style_guide["detail_blue"])

img_slice.show()
