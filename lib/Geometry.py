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
        self.spatial2 = Spatial(x=spatial1.x + spatial1.vx(distance), y=spatial1.y + spatial1.vy(distance), o=spatial1.o)
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_mainfold = (self.spatial1.x, self.spatial1.y, self.spatial2.x, self.spatial2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_mainfold, line_pen)


class Arc(Geometry):
    def __init__(self, spatial1, arc_angle_change, curve_radius):
        super().__init__(spatial1)
        # FIND THE ARC CENTER
        print(spatial1.o)
        o_r = spatial1.o.rad
        displacement_to_center = np.asarray([0, curve_radius])
        rotation_array = np.asarray([[np.cos(o_r), -1*np.sin(o_r)], [np.sin(o_r), np.cos(o_r)]])
        print(displacement_to_center)
        print(rotation_array)
        arc_center = np.asarray(spatial1.t) + np.matmul(rotation_array, displacement_to_center)
        print(arc_center)

        # CREATE THE 2ND SPATIAL
        approach_o = spatial1.o
        approach_p = approach_o - 1
        exit_o = approach_o + arc_angle_change
        exit_p = exit_o - 1
        self.spatial2 = Spatial(x=np.cos(exit_p.deg) * curve_radius + arc_center[0], y=np.sin(exit_p.deg) * curve_radius + arc_center[1], o=exit_o)

        # BUILD THE SHAPELY PSUEDOCURVE
        numsegments = 1000
        theta = np.linspace(spatial1.o.rad, self.spatial2.o.rad, numsegments)
        x = arc_center[0] + curve_radius * np.cos(theta)
        y = arc_center[1] + curve_radius * np.sin(theta)
        self.logic_manifold = LineString(np.column_stack([x, y]))

        # BUILD THE RENDER MANIFOLD
        print(approach_o.inv_deg)
        print(exit_o.inv_deg)
        self.render_mainfold = [(arc_center[0] - curve_radius, arc_center[1] - curve_radius,
                                 arc_center[0] + curve_radius, arc_center[1] + curve_radius),
                                180, 225]

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.arc(self.render_mainfold[0], self.render_mainfold[1], self.render_mainfold[2], line_pen)

class TextBBox(Geometry):
    pass

class Interchange(Geometry):
    pass

class Terminus(Geometry):
    pass

class Station(Geometry):
    pass