from shapely.geometry import Point, LineString
import aggdraw
import numpy as np

from lib.Spatial import Spatial
from lib.degree import degree


class Geometry:
    def __init__(self, spatial1: Spatial):
        self.spatial1 = spatial1
        self.spatial2 = None
        self.logic_manifold = None
        self.render_mainfold = None

    def get_logic(self):
        return self.logic_manifold

    def execute_render(self, *args):
        return


class Straight(Geometry):
    def __init__(self, spatial1: Spatial, distance: int):
        super().__init__(spatial1)
        self.spatial2 = Spatial(x=spatial1.x + spatial1.o.vx(distance), y=spatial1.y + spatial1.o.vy(distance), o=spatial1.o)
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_mainfold = (self.spatial1.x, self.spatial1.y, self.spatial2.x, self.spatial2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_mainfold, line_pen)


class Arc(Geometry):
    def __init__(self, spatial1, arc_angle_change, curve_radius):
        super().__init__(spatial1)
        # FIND THE ARC CENTER
        o_to_center = degree(np.sign(arc_angle_change) * 2 + spatial1.o)
        displacement_to_center = np.asarray([o_to_center.ux * curve_radius, o_to_center.uy * curve_radius])
        arc_center = np.asarray(spatial1.t) + displacement_to_center

        # CREATE THE 2ND SPATIAL
        exit_o = spatial1.o + arc_angle_change
        o_exit_to_center = o_to_center + arc_angle_change
        o_center_to_exit = o_exit_to_center + 4
        self.spatial2 = Spatial(x=o_center_to_exit.ux * curve_radius + arc_center[0],
                                y=o_center_to_exit.uy * curve_radius + arc_center[1], o=exit_o)

        # BUILD THE SHAPELY PSUEDOCURVE
        numsegments = 1000
        theta = np.linspace((o_to_center - 4).rad, o_center_to_exit.rad, numsegments)
        x = arc_center[0] + curve_radius * np.cos(theta)
        y = arc_center[1] + curve_radius * np.sin(theta)
        self.logic_manifold = LineString(np.column_stack([x, y]))

        # BUILD THE RENDER MANIFOLD
        if arc_angle_change > 0:
            arc_angle_1 = o_center_to_exit.inv_deg
            arc_angle_2 = (o_to_center - 4).inv_deg
        else:
            arc_angle_2 = o_center_to_exit.inv_deg
            arc_angle_1 = (o_to_center - 4).inv_deg
        self.render_mainfold = [(arc_center[0] - curve_radius, arc_center[1] - curve_radius,
                                 arc_center[0] + curve_radius, arc_center[1] + curve_radius),
                                arc_angle_1, arc_angle_2]

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.arc(self.render_mainfold[0], self.render_mainfold[1] - 2, self.render_mainfold[2] + 2, line_pen)


class TextBBox(Geometry):
    pass


class InterchangeNode(Geometry):
    def __init__(self, spatial1):
        super().__init__(spatial1)
        self.spatial2 = spatial1
        self.logic_manifold = Point(self.spatial1.t)
        self.render_mainfold = [spatial1.x, spatial1.y, spatial1.x, spatial1.y]

    def execute_render(self, draw: aggdraw.Draw, brush: aggdraw.Brush, radius: int):
        ellipse_bounds = np.asarray(self.render_mainfold) + np.asarray([radius, radius, -1*radius, -1*radius])
        draw.ellipse(tuple(ellipse_bounds), aggdraw.Pen((0, 0, 0, 0), 0, 0), brush)


class HandicapNode(InterchangeNode):
    def __init__(self, spatial1):
        super().__init__(spatial1)

    def execute_render(self, draw: aggdraw.Draw, brush: aggdraw.Brush, radius: int, cpen: aggdraw.Pen, pen: aggdraw.Pen):
        ellipse_bounds = np.asarray(self.render_mainfold) + np.asarray([radius, radius, -1 * radius, -1 * radius])
        draw.ellipse(tuple(ellipse_bounds), cpen, brush)
        segment_list = [[-0.6, 0.5, -0.4, 0],
                        [-0.4, 0, 0.2, 0],
                        [0.2, 0, 0.2, -0.4],
                        [0.2, -0.3, -0.3, -0.3],
                        # Head
                        [0.1, -0.6, 0.3, -0.6],
                        [0.2, -0.5, 0.2, -0.7]]
        arc_bounds = [-0.5, -0.3, 0.5, 0.7]
        for segment in segment_list:
            seg = np.multiply(np.asarray(segment), radius) + np.asarray(self.render_mainfold)
            draw.line(tuple(seg), pen)
        arc_bounds = np.multiply(np.asarray(arc_bounds), radius) + np.asarray(self.render_mainfold)
        draw.arc(tuple(arc_bounds), 225, 45, pen)


class InterchangeConnector(Geometry):
    def __init__(self, spatial1, spatial2):
        super().__init__(spatial1)
        self.spatial2 = spatial2
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_mainfold = (self.spatial1.x, self.spatial1.y, self.spatial2.x, self.spatial2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_mainfold, line_pen)


class Terminus(Geometry):
    def __init__(self, spatial1, tick_length: int):
        super().__init__(spatial1)
        self.spatial2 = spatial1
        station_o_1 = spatial1.o - 2
        station_o_2 = spatial1.o + 2

        self.spatial_t1 = Spatial(x=spatial1.x + station_o_1.vx(tick_length),
                                  y=spatial1.y + station_o_1.vy(tick_length),
                                  o=spatial1.o)
        self.spatial_t2 = Spatial(x=spatial1.x + station_o_2.vx(tick_length),
                                  y=spatial1.y + station_o_2.vy(tick_length),
                                  o=spatial1.o)

        self.logic_manifold = LineString([self.spatial_t1.t, self.spatial_t2.t])
        self.render_mainfold = (self.spatial_t1.x, self.spatial_t1.y, self.spatial_t2.x, self.spatial_t2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_mainfold, line_pen)

class Station(Geometry):
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
        self.render_mainfold = (self.spatial1.x, self.spatial1.y, self.spatial_station.x, self.spatial_station.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_mainfold, line_pen)

