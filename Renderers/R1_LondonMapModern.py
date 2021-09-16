import PIL
from PIL import Image, ImageDraw

import Graph


class R1_LondonMapModern:
    def __init__(self, size, rparams):
        self.image = PIL.Image.new('RGBA', size, (0, 0, 0, 0))

    def render(self, graph):
        for edge in graph.edge_list:
            print([edge.loc1[0], edge.loc1[1], edge.loc2[0], edge.loc2[1]])
            #self.image.ImageDraw.line(,
                                      #fill=edge.color, width=10, joint="curve")
        return self.image

