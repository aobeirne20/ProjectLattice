import PIL

from London.render_lib.rRiver import rRiver

from parameters.StyleGuides import complete_style_guide as csg


class Renderer:
    def __init__(self, art_style):
        self.IMG = PIL.Image.new('RGBA', (csg.xs, csg.ys), (0, 0, 0, 0))
        self.art_style = art_style

    def render(self, tmap):
        self.IMG = rRiver(tmap, self.IMG, self.art_style)

    def return_img(self):
        return self.IMG
