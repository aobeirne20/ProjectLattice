import PIL
from PIL import Image, ImageOps, ImageChops

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
        self.art_style = style_data.StyleDatabase.art_style_guide[art_type]
        self.generated_text = None

        if self.city == 'London':
            self.SD_city = style_data.StyleDatabase.London_style_guide


        self.background_img = None
        self.map = None
        self.generated_img = None
        self.post_process_img = None
        self.final_img = None

        self.size_og = (int(self.SD.map_style_guide[self.city]['x_size'] * self.SD.map_scale),
                        int(self.SD.map_style_guide[self.city]['y_size'] * self.SD.map_scale))
        self.size_s = (int(self.SD.map_style_guide[self.city]['x_size'] * self.SD.t_scale),
                        int(self.SD.map_style_guide[self.city]['y_size'] * self.SD.t_scale))

        # Being active processes
        self.background()
        self.generate()
        self.render()
        self.post_process()

    def background(self):
        background = self.art_style['background']
        if background == 'white':
            self.background_img = PIL.Image.new('RGBA', self.size_s,
                                                self.SD.map_style_guide[self.city]['default_background'])
        elif background == 'black':
            self.background_img = PIL.Image.new('RGBA', self.size_s,
                                                self.SD.map_style_guide[self.city]['dark_background'])
        elif background == 'darkblue':
            self.background_img = PIL.Image.new('RGBA', self.size_s, (53, 85, 123))

    def generate(self):
        generator = citygen_dict[self.city](size_tp=self.size_s)
        self.map = generator.give_map()

    def render(self):
        renderer = cityren_dict[self.city](art_style=self.art_style, size_tp=self.size_s, net_map=self.map)
        self.generated_img, self.generated_text = renderer.give_render()

    def post_process(self):
        details = self.art_style['details']

        if details == 'greyscale' or details == 'inverted greyscale':
            self.post_process_details = ImageOps.grayscale(self.generated_img)
        elif details == 'line' or details == 'inverted line':
            self.post_process_details = self.generated_img
        elif details == 'gold' or details == 'inverted gold':
            self.post_process_details = ImageOps.grayscale(self.generated_img)
            self.post_process_details = PIL.ImageOps.colorize(self.post_process_details,
                                                              (198, 147, 10), (255, 223, 0))
        elif details == 'signature':
            self.post_process_details = self.generated_img
        else:
            self.post_process_details = self.generated_img

        if details == 'inverted' or details == 'inverted line':
            self.post_process_details = self.invert_w_transperancy_colora(self.post_process_details)
        elif details == 'inverted greyscale':
            self.post_process_details = PIL.ImageOps.invert(self.post_process_details)
            #self.post_process_details = self.invert_w_transperancy_grey(self.post_process_details)
        elif details == 'inverted gold':
            self.post_process_details = self.invert_w_transperancy_color(self.post_process_details)


        self.background_img.paste(self.post_process_details, mask=self.generated_img)
        self.post_process_img = self.background_img
        self.post_process_img.paste(self.generated_text, mask=self.generated_text)
        self.final_img = self.post_process_img.resize(self.size_og, resample=PIL.Image.ANTIALIAS)

    def invert_w_transperancy_colora(self, img):
        r, g, b, a = img.split()
        def invert(image):
            return image.point(lambda p: 255 - p)
        r, g, b = map(invert, (r, g, b))
        img2 = Image.merge(img.mode, (r, g, b, a))
        return img2

    def invert_w_transperancy_grey(self, img):
        l = img.split()
        def invert(image):
            return image.point(lambda p: 255 - p)
        l = map(invert, l)
        img2 = Image.merge(img.mode, l)
        return img2

    def invert_w_transperancy_color(self, img):
        r, g, b = img.split()
        def invert(image):
            return image.point(lambda p: 255 - p)
        r, g, b = map(invert, (r, g, b))
        img2 = Image.merge(img.mode, (r, g, b))
        return img2

    def ex_nihilo_res(self):
        return self.final_img, {"REPLACE": "THIS WITH THE ACTUAL METADATA"}
