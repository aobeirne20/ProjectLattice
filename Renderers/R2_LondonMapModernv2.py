import PIL
from PIL import Image, ImageDraw
import random

import Map


class R2_LondonMapModernv2:
    def __init__(self, size, rparams):
        self.image = PIL.Image.new('RGBA', size, (0, 0, 0, 0))
        self.overlay_list = []
        for n in range(0, 14):
            self.overlay_list.append(PIL.Image.new('RGBA', size, (0, 0, 0, 0)))

    def render(self, map):
        draw = ImageDraw.Draw(self.image)
        for feature in map.feature_list:
            if feature.name == "river":
                draw.line(feature.loc_list, (46, 193, 244, 255), width=30, joint="curve")
                draw.line(feature.loc_list, (199, 1234, 252, 255), width=26, joint="curve")

        for line in map.line_list:
            if line.style == "single":
                draw.line(line.loc_list, line.color, width=12, joint="curve")
            elif line.style == "double":
                draw.line(line.loc_list, line.color, width=12, joint="curve")
                draw.line(line.loc_list, (255, 255, 255, 255), width=4, joint="curve")

        return self.image

    def render_brightline(self, map):

        style_guide = [
            {"name": "Emirates Air", "color": (220, 36, 31, 255), "type": 'cable', "style": "double"},
            {"name": "Elizabeth", "color": (147, 100, 204, 255), "type": 'normal', "style": "double"},
            {"name": "DLR", "color": (0, 175, 173, 255), "type": 'light', "style": "double"},
            {"name": "Overground", "color": (239, 123, 16, 255), "type": 'heavy', "style": "double"},
            {"name": "Bakerloo", "color": (178, 99, 0, 255), "type": 'normal', "style": "single"},
            {"name": "Central", "color": (220, 36, 31, 255), "type": 'normal', "style": "single"},
            {"name": "Circle", "color": (255, 211, 41, 255), "type": 'circle', "style": "single"},
            {"name": "District", "color": (0, 125, 50, 255), "type": 'normal', "style": "single"},
            {"name": "H'smith & City", "color": (244, 169, 190, 255), "type": 'normal', "style": "single"},
            {"name": "Jubilee", "color": (161, 165, 167, 255), "type": 'normal', "style": "single"},
            {"name": "Metropolitan", "color": (155, 0, 88, 255), "type": 'normal', "style": "single"},
            {"name": "Northern", "color": (0, 0, 0, 255), "type": 'normal', "style": "single"},
            {"name": "Picadilly", "color": (0, 25, 168, 255), "type": 'normal', "style": "single"},
            {"name": "Victoria", "color": (0, 152, 216, 255), "type": 'normal', "style": "single"},
            {"name": "Waterloo & City", "color": (147, 206, 186, 255), "type": 'shuttle', "style": "single"},
        ]

        for n in range(0, 14):
            draw = ImageDraw.Draw(self.overlay_list[n])

            line_color = style_guide[n]["color"]
            line_style = style_guide[n]["style"]

            for line in map.line_list:
                if (line.color == line_color) & (line.style == line_style):
                    if line.style == "single":
                        draw.line(line.loc_list, line.color, width=12, joint="curve")
                    elif line.style == "double":
                        draw.line(line.loc_list, line.color, width=12, joint="curve")
                        draw.line(line.loc_list, (255, 255, 255, 255), width=4, joint="curve")

        return self.overlay_list




