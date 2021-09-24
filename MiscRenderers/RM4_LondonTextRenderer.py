import geometric_elements as ge
import aggdraw
import math

import PIL
from PIL import Image, ImageDraw, ImageFont
import style_data as sd
import names_london as names

class RM4_LondonTextRenderer():
    def __init__(self, text_loc_list, xs, ys, text_giver):
        self.xs = xs
        self.ys = ys
        self.text_loc_list = text_loc_list
        self.text_giver = text_giver

    def render(self):
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img_slice)
        font = ImageFont.truetype("Railway-Semibold.ttf", 60)
        for station in self.text_loc_list:
            name = self.text_giver.give_name(station['type'])
            draw.text(station['location'], name, font=font, fill=(0, 0, 0, 255))
        return img_slice

