import Network
import numpy
from PIL import Image, ImageDraw, ImageColor, ImageMode


class RenderEngine:
    def __init__(self, canvas, graph):
        draw = ImageDraw.Draw(canvas)
        for vertex in graph.vertex_list:
            corners = [vertex.position[0]-12, vertex.position[1]-12, vertex.position[0]+12, vertex.position[1]+12]
            draw.ellipse(corners, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
