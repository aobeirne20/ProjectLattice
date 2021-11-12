import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from map_lib.Line import Line
from color_lib.ColorOps import invert_color, greyscale_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg

def rInterchange(tmap: TMap, interchange_list, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    asg_b = asg['background']

    outside_color = csg.palette_style_guide['black']
    inside_color = csg.palette_style_guide['white']

    if asg_b == 'black':
        outside_color, inside_color = inside_color, outside_color

    outside_brush = aggdraw.Brush(outside_color)
    inside_brush = aggdraw.Brush(inside_color)

    for interchange in interchange_list:
        if interchange is not None:
            interchange.execute_render(draw, outside_brush, opt.interchange_render_outer_radius)
            interchange.execute_render(draw, inside_brush, opt.interchange_render_inner_radius)

    draw.flush()

    return IMG
