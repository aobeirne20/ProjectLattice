import PIL
from PIL import Image

from Generators import G1_TransitMap
from Renderers import R1_LondonMapModern

gen_dict = {"G1_TransitMap": G1_TransitMap.G1_TransitMap}
rend_dict = {"R1_LondonMapModern": R1_LondonMapModern.R1_LondonMapModern}


class ImageGen:
    def __init__(self, size):
        self.size = size
        self.background_image = None
        self.render_image = None
        self.graph = None
        self.metadata = None

    def background(self, background_colors, background_img):
        if background_img is None:
            self.background_image = PIL.Image.new('RGBA', self.size, background_colors)
        else:
            return  # Add this functionality

    def generate(self, generator_name, gparams):
        generator = gen_dict[generator_name](size=self.size, gparams=gparams)
        self.graph = generator.generate()
        print(f"{generator_name} generation complete")

    def render(self, renderer_name, rparams):
        renderer = rend_dict[renderer_name](size=self.size, rparams=rparams)
        self.render_image = renderer.render(self.graph)
        print(f"{renderer_name} render complete")

    def show(self):
        self.render_image.show()
        self.background_image.paste(self.render_image, mask=self.render_image)
        self.background_image.show()
