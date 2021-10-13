from lib.degree import degree
from lib.Geometry import Geometry, Straight, Arc
from lib.Spatial import Spatial

import aggdraw
import PIL

s1 = Spatial(x=200, y=200, o=degree(-3))
a = Straight(s1, 100)
print(a.spatial2.t)
b = Arc(a.spatial2, 2, 50)

print(b.render_mainfold)

pen = aggdraw.Pen((255, 255, 255, 255), 20)
img_slice = PIL.Image.new('RGBA', (500, 500), color=(20, 80, 200, 255))
draw = aggdraw.Draw(img_slice)

a.execute_render(draw, pen)
b.execute_render(draw, pen)
draw.flush()
img_slice.show()

from math import radians, sin, cos, sqrt, asin


def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c

print(haversine(47.64989825, -122.30484132, 47.64989825, -122.30484064) * 1000)

