import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from map_lib.Line import Line
from color_lib.ColorOps import invert_color, greyscale_color, goldshade_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def rLine(tmap: TMap, line: Line, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    asg_d, asg_b = asg['details'], asg['background']
    lsg = line.style_details

    # ------------------------------------------------------------------------------------------------------------------
    # LINE COLORS
    line_color = lsg['color']

    if asg_d == 'inverted' or asg_d == 'inverted greyscale' or asg_d == 'inverted line':
        line_color = invert_color(line_color)

    if asg_d == 'greyscale' or asg_d == 'inverted greyscale':
        line_color = greyscale_color(line_color)





    if asg_d == 'gold' or asg_d == 'inverted gold':
        line_color = goldshade_color(line_color)
        if asg_d == 'inverted gold':
            line_color = invert_color(line_color)

    if line_color == csg.palette_style_guide[asg_b]:
        line_color = invert_color(line_color)


    label_color = csg.palette_style_guide['black']



    line_pen = aggdraw.Pen(line_color, opt.single_line_width)
    mid_pen = aggdraw.Pen(csg.palette_style_guide[asg_b], opt.double_line_inner_width)
    station_pen = aggdraw.Pen(line_color, opt.station_tick_width)

    # RENDERING
    if asg_b == 'darkblue':
        white_outline_pen = aggdraw.Pen(csg.palette_style_guide['white'], opt.single_line_width)
        line_pen = aggdraw.Pen(line_color, opt.night_tube_inline_width)
        for branch in line.branches:
            for geometry in branch.segment_list:
                if geometry is not None:
                    geometry.execute_render(draw, white_outline_pen)
            for station in branch.station_list:
                if station is not None:
                    station.execute_render(draw, white_outline_pen)

    for branch in line.branches:
        for station in branch.station_list:
            if station is not None:
                if asg_b == 'darkblue':
                    station.execute_render(draw, station_pen, True)
                else:
                    station.execute_render(draw, station_pen)


    for branch in line.branches:
        for geometry in branch.segment_list:
            if geometry is not None:
                geometry.execute_render(draw, line_pen)

    if lsg['line_type'] == 'double':
        for branch in line.branches:
            for geometry in branch.segment_list:
                if geometry is not None:
                    geometry.execute_render(draw, mid_pen)

    draw.flush()
    idraw = ImageDraw.Draw(IMG)


    for branch in line.branches:
        for label in branch.label_list:
            if label is not None:
                label.execute_render(idraw, label_color)

    return IMG