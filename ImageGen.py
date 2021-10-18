import PIL
from PIL import Image, ImageOps, ImageChops


class ImageGen:
    def __init__(self, city, art_type):
        self.final_img = PIL.Image.new('RGBA', (500, 500), color=(200, 80, 100, 255))

    def ex_nihilo_res(self):
        return self.final_img, {"REPLACE": "THIS WITH THE ACTUAL METADATA"}