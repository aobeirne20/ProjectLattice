import PIL
from PIL import Image

import CompleteStyleGuide
import CompleteMaterializer


class ImageGen:
    def __init__(self, city, art_type):
        self.city = city
        self.art_type = art_type
        self.csg = CompleteStyleGuide.CompleteStyleGuide(city)
        self.cm = CompleteMaterializer.CompleteMaterializer(city, self.csg)

        # NONE ASSIGNS FOR LATER
        self.MAP_topological = None
        self.background_color = None
        self.IMG_background = None
        self.IMG_final = None
        self.IMG_render = None

        self.background()
        self.generate()
        self.render()
        self.post_process()

    def background(self):
        background_name = self.csg.art_style_guide[self.art_type]['background']
        self.background_color = self.csg.palette_style_guide[background_name]
        self.IMG_background = PIL.Image.new('RGBA', (self.csg.xs, self.csg.ys), self.background_color)

    def generate(self):
        self.cm.generator.generate()
        self.MAP_topological = self.cm.generator.return_map()

    def render(self):
        self.cm.renderer.render(self.MAP_topological)
        self.IMG_render = self.cm.renderer.return_img()

    def post_process(self):
        self.IMG_background.paste(self.IMG_render, mask=self.IMG_render)
        self.IMG_final = self.IMG_background

    def ex_nihilo_res(self):
        return self.IMG_final, {"REPLACE": "THIS WITH THE ACTUAL METADATA"}



