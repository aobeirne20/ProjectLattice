import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from map_lib.Line import Line
from color_lib.ColorOps import invert_color, greyscale_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg

def rInterchange(tmap: TMap, interchange, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]

    black_brush = aggdraw.Brush(csg.palette_style_guide['black'])
    white_brush = aggdraw.Brush(csg.palette_style_guide['white'])

    interchange.execute_render(draw, black_brush, opt.interchange_render_outer_radius)
    interchange.execute_render(draw, white_brush, opt.interchange_render_inner_radius)

    draw.flush()

    return IMG
