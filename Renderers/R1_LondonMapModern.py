import PIL
from PIL import Image, ImageDraw

import Graph


class R1_LondonMapModern:
    def __init__(self, size, rparams):
        self.image = PIL.Image.new('RGBA', size, (0, 0, 0, 0))

    def render(self, graph):
        for edge in graph.edge_list:
            linep = [edge.loc1[0], edge.loc1[1], edge.loc2[0], edge.loc2[1]]
            draw = ImageDraw.Draw(self.image)
            draw.line(linep, fill=edge.color, width=8, joint="curve")
        return self.image

