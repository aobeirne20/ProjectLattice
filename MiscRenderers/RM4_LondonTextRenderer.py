import geometric_elements as ge
import aggdraw
import math

import PIL
from PIL import Image, ImageDraw, ImageFont
import style_data as sd
import numpy as np

anchor_dict = {0: 'lm', 45: 'ld', 90: 'md', 135: 'rd', 180: 'rm', 225: 'ra', 270: 'ma', 315: 'la', 999: 'lm'}

class RM4_LondonTextRenderer():
    def __init__(self, text_loc_list, xs, ys, text_giver, text_color):
        self.xs = xs
        self.ys = ys
        self.sd = sd
        self.text_loc_list = text_loc_list
        self.text_giver = text_giver
        self.text_color = text_color

    def render(self):
        img_slice = PIL.Image.new('RGBA', (self.xs, self.ys), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img_slice)
        font = ImageFont.truetype("ITC - JohnstonITCPro-Medium.otf", 25*self.sd.StyleDatabase.t_scale)
        for station in self.text_loc_list:
            if station['name'] == 'Single':
                pass
            else:
                name = station['text']
                draw.multiline_text(station['text_location'], name, font=font, align='center', fill=self.text_color, anchor=anchor_dict[station['orientation']])
        return img_slice

