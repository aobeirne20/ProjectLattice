import PIL

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

        for line in tmap.line_list:
            self.IMG = rLine(tmap, line, self.IMG, self.art_style)

        for interchange in tmap.interchange_list:
            self.IMG = rInterchange(tmap, interchange, self.IMG, self.art_style)

    def return_img(self):
        return self.IMG
