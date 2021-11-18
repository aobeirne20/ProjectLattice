import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from color_lib.ColorOps import invert_color, greyscale_color, goldshade_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def rRiver(tmap: TMap, river, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    asg_r = asg['river']
    inner_width = opt.river_inner_width
    outer_width = opt.river_outer_width


    if asg['background'] == 'darkblue':
        fill_color = csg.palette_style_guide['night_river_fill']
        border_color = csg.palette_style_guide['night_river_border']
    elif asg['background'] == 'black':
        fill_color = csg.palette_style_guide['dark_river_fill']
        border_color = csg.palette_style_guide['dark_river_border']
    elif asg_r == 'gold' or asg_r == 'inverted gold':
        if asg['background'] == 'black':
            fill_color = csg.palette_style_guide['black']
            border_color = csg.palette_style_guide['white']
        else:
            fill_color = csg.palette_style_guide['white']
            border_color = csg.palette_style_guide['black']
    else:
        fill_color = csg.palette_style_guide['river_fill']
        border_color = csg.palette_style_guide['river_border']



    if asg_r == 'gold' or asg_r == 'inverted gold':
        fill_color = goldshade_color(fill_color)
        border_color = goldshade_color(border_color)

    if asg_r == 'greyscale' or asg_r == 'inverted greyscale' or asg_r == 'inverted gold':
        fill_color = greyscale_color(fill_color)
        border_color = greyscale_color(border_color)


    outer_pen = aggdraw.Pen(border_color, outer_width)
    inner_pen = aggdraw.Pen(fill_color, inner_width)

    for piece in river.render_list:
        piece.execute_render(draw, outer_pen)
    for piece in river.render_list:
        piece.execute_render(draw, inner_pen)

    draw.flush()
    idraw = ImageDraw.Draw(IMG)

    for label in river.label_list:
        label.execute_render(idraw, border_color)

    return IMG
