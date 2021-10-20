import PIL

from London.render_lib.rRiver import rRiver


class Renderer:
    def __init__(self, csg):
        self.csg = csg
        self.IMG = PIL.Image.new('RGBA', (csg.xs, csg.ys), (0, 0, 0, 0))

    def render(self, tmap):
        self.IMG = rRiver(self.csg, tmap, self.IMG)

    def return_img(self):
        return self.IMG
