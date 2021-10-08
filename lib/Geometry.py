from shapely.geometry import Point, LineString

from Spatial import Spatial
import degree


class Geometry:
    def __init__(self, spatial1: degree):
        pass


class Straight(Geometry):
    def __init__(self, spatial1: Spatial, distance: int):
        self.spatial1 = spatial1
        self.spatial2 = Spatial(x=spatial1.x + spatial1.vx(distance), y=spatial1.y + spatial1.vy(distance), o=spatial1.o)
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_manifold =
        super().__init__()


class Arc45(Geometry):
    def __init__(self, spatial1, is_negative):
        super().__init__()


class Arc90(Geometry):
    def __init__(self, spatial1, is_negative):
        super().__init__()