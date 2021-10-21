########################################################################################################
# COMPLETE STYLE GUIDE ---------------------------------------------------------------------------------
# LONDON -----------------------------------------------------------------------------------------------
########################################################################################################

from parameters.art_styles import AS1_London
from parameters.line_styles import LS1_London
from parameters.map_styles import MS1_London
from parameters.name_styles import NS1_London
from parameters.palette_styles import PS1_London
from options import prime as opt

csg_file_name = "London"

art_style_guide = AS1_London.art_style_guide
line_style_guide = LS1_London.line_style_guide
map_style_guide = MS1_London.map_style_guide
name_pool = NS1_London.import_pool
palette_style_guide = PS1_London.palette_style_guide

x = map_style_guide["x_size"] * opt.s_outputimage
y = map_style_guide["y_size"] * opt.s_outputimage
xs = map_style_guide["x_size"] * opt.s_combined
ys = map_style_guide["y_size"] * opt.s_combined

