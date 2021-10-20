from parameters.art_styles import AS1_London
from parameters.line_styles import LS1_London
from parameters.map_styles import MS1_London
from parameters.name_styles import NS1_London
from parameters.palette_styles import PS1_London
from options import prime as opt


class CompleteStyleGuide:
    def __init__(self, city):
        if city == 'London':
            self.art_style_guide = AS1_London.art_style_guide
            self.line_style_guide = LS1_London.line_style_guide
            self.map_style_guide = MS1_London.map_style_guide
            self.name_pool = NS1_London.import_pool
            self.palette_style_guide = PS1_London.palette_style_guide
            self.xs = self.map_style_guide["x_size"] * opt.s_combined
            self.ys = self.map_style_guide["y_size"] * opt.s_combined

