import PIL
from PIL import Image, ImageOps

from Generators import G1_TransitMap, G2_TransitMapv2
from Renderers import R1_LondonMapModern, R2_LondonMapModernv2

gen_dict = {"G1_TransitMap": G1_TransitMap.G1_TransitMap,
            "G2_TransitMapv2": G2_TransitMapv2.G2_TransitMapv2}
rend_dict = {"R1_LondonMapModern": R1_LondonMapModern.R1_LondonMapModern,
             "R2_LondonMapModernv2": R2_LondonMapModernv2.R2_LondonMapModernv2}


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
        graph = generator.generate
        graph = generator.gen_features(graph)
        self.graph = graph
        print(f"{generator_name} generation complete")

    def render(self, renderer_name, rparams):
        renderer = rend_dict[renderer_name](size=self.size, rparams=rparams)
        self.render_image = renderer.render(self.graph)
        self.brightline_render_list = renderer.render_brightline(self.graph)
        print(f"{renderer_name} render complete")

    def show(self):
        self.background_image.paste(self.render_image, mask=self.render_image)
        self.background_image.show()
        self.background_image.save("gen_image.png")

    def invert(self):
        r, g, b, a = self.background_image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        self.inverted_image = Image.merge('RGBA', (r2, g2, b2, a))
        self.inverted_image.show()
        self.inverted_image.save("gen_inv_image.png")

    def grayscale(self):
        self.gray = self.background_image.convert('L')
        self.gray.show()
        self.gray.save("gen_gray_image.png")

        self.gray_inv = self.inverted_image.convert('L')
        self.gray_inv.show()
        self.gray_inv.save("gen_gray_inv_image.png")

    def goldscale(self):
        goldscale = PIL.ImageOps.colorize(self.gray, (255, 215, 0), (255, 255, 255))
        goldscale.show()
        goldscale.save("gen_gold_image.png")

        goldscale_inv = PIL.ImageOps.colorize(self.gray_inv, (0, 0, 0), (255, 215, 0))
        goldscale_inv.show()
        goldscale_inv.save("gen_gold_inv_image.png")

    def brightline(self):
        for n in range(0, 14):
            self.temp = self.gray.convert("RGBA")
            self.temp.paste(self.brightline_render_list[n], mask=self.brightline_render_list[n])
            self.temp.show()
            self.temp.save(f"gen_brightline + {n}_image.png")





