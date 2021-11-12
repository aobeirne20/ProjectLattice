import PIL
import numpy as np

from London.render_lib.rRiver import rRiver
from London.render_lib.rLine import rLine
from London.render_lib.rInterchange import rInterchange

from parameters.StyleGuides import complete_style_guide as csg


class Renderer:
    def __init__(self, art_style):
        self.IMG = PIL.Image.new('RGBA', (csg.xs, csg.ys), (0, 0, 0, 0))
        self.art_style = art_style

    def render(self, tmap):
        for thing in tmap.feature_list:
            if thing.feature_type_name == 'River':
                self.IMG = rRiver(tmap, thing, self.IMG, self.art_style)

        if csg.art_style_guide[self.art_style]['details'] == 'line' or csg.art_style_guide[self.art_style]['details'] == 'inverted line':
            self.brightline_handler(tmap, self.IMG, self.art_style)
        else:
            for line in tmap.line_list:
                self.IMG = rLine(tmap, line, self.IMG, self.art_style)

        self.IMG = rInterchange(tmap, tmap.interchange_list, self.IMG, self.art_style)

    def brightline_handler(self, tmap, IMG, art_style):
        bright_line = np.random.choice(tmap.line_list)
        tmap.line_list.remove(bright_line)

        if self.art_style == "Brightline":
            single_type = "Color"
            group_type = "Grey"
        elif self.art_style == "Anti-brightline":
            single_type = "Anti-color"
            group_type = "Anti-grey"
        elif self.art_style == "Darkline":
            single_type = "Dark"
            group_type = "Dark Grey"
        elif self.art_style == "Anti-darkline":
            single_type = "Anti-dark"
            group_type = "Dark Anti-grey"
        else:
            raise ValueError()

        self.IMG = rLine(tmap, bright_line, self.IMG, single_type)
        for line in tmap.line_list:
            self.IMG = rLine(tmap, line, self.IMG, group_type)

    def return_img(self):
        return self.IMG
