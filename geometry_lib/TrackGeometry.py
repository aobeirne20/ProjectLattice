from shapely.geometry import LineString
import aggdraw
import numpy as np

from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.Geometry import Geometry


class TrackGeometry(Geometry):
    def __init__(self, spatial1):
        super().__init__()
        self.spatial1 = spatial1


class Straight(TrackGeometry):
    def __init__(self, spatial1: Spatial, distance: int):
        super().__init__(spatial1)
        self.spatial2 = Spatial(x=spatial1.x + spatial1.o.vx(distance), y=spatial1.y + spatial1.o.vy(distance), o=spatial1.o)
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_manifold = (self.spatial1.x, self.spatial1.y, self.spatial2.x, self.spatial2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_manifold, line_pen)


class Arc(TrackGeometry):
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
        t1, t2 = (o_to_center - 4).rad, o_center_to_exit.rad
        if np.sign(arc_angle_change) == 1 and o_center_to_exit == 0:
            t2 = 2*np.pi
        elif (o_to_center - 4) == 0 and np.sign(arc_angle_change) == -1:
            t1 = 2*np.pi

        theta = np.linspace(t1, t2, numsegments)
        x = arc_center[0] + curve_radius * np.cos(theta)
        y = arc_center[1] + curve_radius * np.sin(theta)
        self.logic_manifold = LineString(np.column_stack([x, y]))

        # BUILD THE RENDER MANIFOLD
        arc_angle_1 = o_center_to_exit.inv_deg
        arc_angle_2 = (o_to_center - 4).inv_deg
        if arc_angle_change <= 0:
            arc_angle_2, arc_angle_1 = arc_angle_1, arc_angle_2
        self.render_manifold = [(arc_center[0] - curve_radius, arc_center[1] - curve_radius,
                                 arc_center[0] + curve_radius, arc_center[1] + curve_radius),
                                arc_angle_1, arc_angle_2]

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.arc(self.render_manifold[0], self.render_manifold[1] - 2, self.render_manifold[2] + 2, line_pen)
