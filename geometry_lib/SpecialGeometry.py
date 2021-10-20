from shapely.geometry import Point, LineString
import aggdraw
import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.Geometry import Geometry


class SpecialGeometry(Geometry):
    def __init__(self, spatial1):
        super().__init__()
        self.spatial1 = spatial1


class TextBBox(SpecialGeometry):
    pass


class RailLogo(SpecialGeometry):
    pass
