import PIL
from PIL import Image, ImageOps

import style_data
from CityGenerators import G1_London, G2_Paris, G3_NewYork, G4_Moscow, G5_Tokyo, G6_Beijing
from CityRenderers import R1_London, R2_Paris, R3_NewYork, R4_Moscow, R5_Tokyo, R6_Beijing
citygen_dict = {"London": G1_London.G1_London, "Paris": G2_Paris.G2_Paris, "NewYork": G3_NewYork.G3_NewYork,
                "Moscow": G4_Moscow.G4_Moscow, "Tokyo": G5_Tokyo.G5_Tokyo, "Beijing": G6_Beijing.G6_Beijing}
cityren_dict = {"London": R1_London.R1_London, "Paris": R2_Paris.R2_Paris, "NewYork": R3_NewYork.R3_NewYork,
                "Moscow": R4_Moscow.R4_Moscow, "Tokyo": R5_Tokyo.R5_Tokyo, "Beijing": R6_Beijing.R6_Beijing}


class ImageGen:
    def __init__(self, city, art_type):
        self.city = city
        self.art_type = art_type
        self.SD = style_data.StyleDatabase

        self.background_img = None
        self.map = None
        self.generated_img = None
        self.post_process_img = None
        self.final_img = None

        self.size_tp = (self.SD.map_style_guide[self.city]['x_size'], self.SD.map_style_guide[self.city]['y_size'])

        # Being active processes
        self.background()
        self.generate()
        self.render()

    def background(self):
        if self.art_type == "Dark" or self.art_type == "Dark_Invert":
            self.background_img = PIL.Image.new('RGBA', self.size_tp,
                                                self.SD.map_style_guide[self.city]['dark_background'])
        else:
            self.background_img = PIL.Image.new('RGBA', self.size_tp,
                                                self.SD.map_style_guide[self.city]['default_background'])

    def generate(self):
        generator = citygen_dict[self.city](art_type=self.art_type, size_tp=self.size_tp)
        self.map = generator.give_map()

    def render(self):
        renderer = cityren_dict[self.city](art_type=self.art_type, size_tp=self.size_tp, mapp=self.map)
        #self.generated_img = renderer.give_render()

    def post_process(self):
        pass

    def ex_nihilo_res(self):
        return self.final_img
