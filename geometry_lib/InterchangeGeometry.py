from shapely.geometry import Point, LineString
import aggdraw
import numpy as np

from geometry_lib.Geometry import Geometry


class InterchangeGeometry(Geometry):
    def __init__(self, spatial1):
        super().__init__()
        self.spatial1 = spatial1
        self.spatial2 = spatial1
        self.logic_manifold = Point(self.spatial1.t)
        self.render_manifold = [spatial1.x, spatial1.y, spatial1.x, spatial1.y]


class InterchangeNode(InterchangeGeometry):
    def __init__(self, spatial1):
        super().__init__(spatial1)

    def execute_render(self, draw: aggdraw.Draw, brush: aggdraw.Brush, radius: int):
        ellipse_bounds = np.asarray(self.render_manifold) + np.asarray([radius, radius, -1*radius, -1*radius])
        draw.ellipse(tuple(ellipse_bounds), aggdraw.Pen((0, 0, 0, 0), 0, 0), brush)


class DarkNode(InterchangeGeometry):
    def __init__(self, spatial1):
        super().__init__(spatial1)
        self.logic_manifold = None
        self.render_mainfold = None

    def execute_render(self, draw: aggdraw.Draw, brush: aggdraw.Brush, radius: int):
        return


class HandicapNode(InterchangeGeometry):
    def __init__(self, spatial1):
        super().__init__(spatial1)

    def execute_render(self, draw: aggdraw.Draw, brush: aggdraw.Brush, radius: int, cpen: aggdraw.Pen, pen: aggdraw.Pen):
        ellipse_bounds = np.asarray(self.render_manifold) + np.asarray([radius, radius, -1 * radius, -1 * radius])
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
            seg = np.multiply(np.asarray(segment), radius) + np.asarray(self.render_manifold)
            draw.line(tuple(seg), pen)
        arc_bounds = np.multiply(np.asarray(arc_bounds), radius) + np.asarray(self.render_manifold)
        draw.arc(tuple(arc_bounds), 225, 45, pen)


class InterchangeConnector(Geometry):
    def __init__(self, spatial1, spatial2):
        super().__init__()
        self.spatial1 = spatial1
        self.spatial2 = spatial2
        self.logic_manifold = LineString([self.spatial1.t, self.spatial2.t])
        self.render_manifold = (self.spatial1.x, self.spatial1.y, self.spatial2.x, self.spatial2.y)

    def execute_render(self, draw: aggdraw.Draw, line_pen: aggdraw.Pen):
        draw.line(self.render_manifold, line_pen)