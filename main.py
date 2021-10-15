from lib.degree import degree
from lib.Geometry import Geometry, Straight, Arc, Station, Terminus
from lib.Spatial import Spatial

import aggdraw
import PIL

s1 = Spatial(x=200, y=200, o=degree(1))
a = Straight(s1, 100)
b = Arc(a.spatial2, -3, 50)
c = Arc(b.spatial2, 1, 100)
d = Station(a.spatial2, True, 30)
e = Terminus(c.spatial2, 30)

pen = aggdraw.Pen((255, 255, 255, 255), 20)
img_slice = PIL.Image.new('RGBA', (500, 500), color=(20, 80, 200, 255))
draw = aggdraw.Draw(img_slice)

a.execute_render(draw, pen)
b.execute_render(draw, pen)
c.execute_render(draw, pen)
d.execute_render(draw, pen)
e.execute_render(draw, pen)
draw.flush()
img_slice.show()

