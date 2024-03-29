from shapely.geometry import LineString
import aggdraw

import options.prime as opt
from geometry_lib.Spatial import Spatial
from geometry_lib.Geometry import Geometry


class StationGeometry(Geometry):
    def __init__(self, spatial1):
        super().__init__()
        self.spatial1 = spatial1
        self.spatial2 = spatial1
        self.spatial_station = None

    def get_text_anchor(self):
        return self.spatial_station


class Terminus(StationGeometry):
    def __init__(self, spatial1, opposite: bool, tick_length: int):
        super().__init__(spatial1)
        self.spatial2 = spatial1
        station_o_1 = spatial1.o - 2
        station_o_2 = spatial1.o + 2

        spatial_t1 = Spatial(x=spatial1.x + station_o_1.vx(tick_length),
                                  y=spatial1.y + station_o_1.vy(tick_length),
                                  o=station_o_1)
        spatial_t2 = Spatial(x=spatial1.x + station_o_2.vx(tick_length),
                                  y=spatial1.y + station_o_2.vy(tick_length),
                                  o=station_o_2)

        if opposite:
            self.spatial_station = spatial_t2
        else:
            self.spatial_station = spatial_t1

        self.logic_manifold = LineString([spatial_t1.t, spatial_t2.t])
        self.render_manifold = (spatial_t1.x, spatial_t1.y, spatial_t2.x, spatial_t2.y)
        self.opposite = opposite

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen, shorten_for_night_tube=False):
        if shorten_for_night_tube is False:
            draw.line(self.render_manifold, line_pen)
        else:
            new_station = Terminus(self.spatial1, self.opposite, opt.inner_station_tick_width)
            draw.line(new_station.render_manifold, line_pen)


class Station(StationGeometry):
    def __init__(self, spatial1, opposite: bool, tick_length: int):
        super().__init__(spatial1)
        self.spatial2 = spatial1
        if opposite:
            station_o = spatial1.o - 2
        else:
            station_o = spatial1.o + 2

        self.spatial_station = Spatial(x=spatial1.x + station_o.vx(tick_length),
                                       y=spatial1.y + station_o.vy(tick_length),
                                       o=station_o)
        self.logic_manifold = LineString([self.spatial1.t, self.spatial_station.t])
        self.render_manifold = (self.spatial1.x, self.spatial1.y, self.spatial_station.x, self.spatial_station.y)
        self.opposite = opposite

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen, shorten_for_night_tube=False):
        if shorten_for_night_tube is False:
            draw.line(self.render_manifold, line_pen)
        else:
            new_station = Station(self.spatial1, self.opposite, opt.inner_station_tick_width)
            draw.line(new_station.render_manifold, line_pen)
