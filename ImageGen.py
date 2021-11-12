import PIL
from PIL import Image

import CompleteMaterializer

from parameters.StyleGuides import complete_style_guide as csg

class ImageGen:
    def __init__(self, city, art_style):
        self.city = city
        self.art_style = art_style
        self.cm = CompleteMaterializer.CompleteMaterializer(city, art_style)

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
        self.metadata()

    def background(self):
        background_name = csg.art_style_guide[self.art_style]['background']
        self.background_color = csg.palette_style_guide[background_name]
        self.IMG_background = PIL.Image.new('RGBA', (csg.xs, csg.ys), self.background_color)

    def generate(self):
        self.cm.generator.generate()
        self.MAP_topological = self.cm.generator.return_map()

    def render(self):
        self.cm.renderer.render(self.MAP_topological)
        self.IMG_render = self.cm.renderer.return_img()

    def post_process(self):
        self.IMG_background.paste(self.IMG_render, mask=self.IMG_render)
        self.IMG_final = self.IMG_background.resize((csg.x, csg.y), resample=PIL.Image.ANTIALIAS)

    def metadata(self):
        self.cm.metadata.add_art_attributes(art_style=self.art_style)
        self.cm.metadata.add_gen_attributes(num_stations=self.cm.generator.get_station_count(),
                                            num_interchanges=self.cm.generator.get_interchange_count(),
                                            len_trackage=self.cm.generator.get_track_mileage())

    def ex_nihilo_res(self):
        return self.IMG_final, self.cm.metadata.meta_dict



