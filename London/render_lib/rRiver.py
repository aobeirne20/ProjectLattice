import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from color_lib.ColorOps import invert_color, greyscale_color, goldshade_color, darken_to_p

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def rRiver(tmap: TMap, river, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    asg_r, asg_b = asg['river'], asg['background']
    inner_width, outer_width = opt.river_inner_width, opt.river_outer_width

    # ------------------------------------------------------------------------------------------------------------------
    # BASE ASSIGNMENT
    if asg_r == 'night':
        border_color = csg.palette_style_guide["night_river_border"]
        fill_color = csg.palette_style_guide["night_river_fill"]
    elif asg_r == 'gold' or asg_r == 'inverted gold':
        border_color = csg.palette_style_guide['black']
        fill_color = (190, 190, 190, 255)#csg.palette_style_guide['white']
    else:
        border_color = csg.palette_style_guide["river_border"]
        fill_color = csg.palette_style_guide["river_fill"]

    # STEP 1: GREYSCALE FOR GRAYS
    if asg_r == 'greyscale':
        border_color, fill_color = greyscale_color(border_color), greyscale_color(fill_color)

    # STEP 2: GOLDSHADE FOR GOLDS
    if asg_r == 'gold' or asg_r == 'inverted gold':
        border_color, fill_color = goldshade_color(border_color), goldshade_color(fill_color)

    # STEP 3: SWITCH FOR DARKS
    if asg_b == 'black':
        border_color, fill_color = fill_color, border_color

    # STEP 4: INVERT FOR INVERTS
    if asg_r == 'inverted gold':
        border_color, fill_color = invert_color(border_color), invert_color(fill_color)
        border_color, fill_color = fill_color, border_color

    # STEP 5: DARKEN FOR DARKS
    if asg_b == 'black':
        border_color, fill_color = darken_to_p(border_color, 0.5), darken_to_p(fill_color, 0.2)
    # ------------------------------------------------------------------------------------------------------------------

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
