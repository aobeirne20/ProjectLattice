import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from color_lib.ColorOps import invert_color, greyscale_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def rRiver(tmap: TMap, IMG, art_style):
    draw = aggdraw.Draw(IMG)

    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    fill_color = csg.palette_style_guide['river_fill']
    border_color = csg.palette_style_guide['river_border']
    inner_width = opt.river_inner_width
    outer_width = opt.river_outer_width

    if asg['river'] == 'normal':
        pass
    elif asg['river'] == 'inverted':
        fill_color = invert_color(fill_color)
        border_color = invert_color(border_color)
    elif asg['river'] == 'greyscale':
        fill_color = greyscale_color(fill_color)
        border_color = greyscale_color(border_color)
    elif asg['river'] == 'inverted greyscale':
        fill_color = greyscale_color(fill_color)
        border_color = greyscale_color(border_color)
        fill_color = invert_color(fill_color)
        border_color = invert_color(border_color)
    elif asg['river'] == 'gold':
        pass
    elif asg['river'] == 'inverted gold':
        fill_color = invert_color(fill_color)
        border_color = invert_color(border_color)
    else:
        raise KeyError('River style not found in ASG')

    outer_pen = aggdraw.Pen(border_color, outer_width)
    inner_pen = aggdraw.Pen(fill_color, inner_width)

    for feature in tmap.feature_list:
        for thing in feature.render_list:
            thing.execute_render(draw, outer_pen)
        for thing in feature.render_list:
            thing.execute_render(draw, inner_pen)

    draw.flush()
    idraw = ImageDraw.Draw(IMG)

    for feature in tmap.feature_list:
        for label in feature.label_list:
            label.execute_render(idraw, border_color)


    return IMG
