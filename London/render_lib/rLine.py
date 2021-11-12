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
    asg_d = asg['details']
    asg_b = asg['background']
    lsg = line.style_details
    line_color = lsg['color']
    mid_color = csg.palette_style_guide['white']

    # LINE COLORING
    if asg_d == 'greyscale' or asg_d == 'inverted greyscale':
        line_color = greyscale_color(line_color)

    if asg_d == 'gold' or asg_d == 'inverted gold':
        line_color = goldshade_color(line_color)

    if asg_d == 'inverted' or asg_d == 'inverted gold' or asg_d == 'inverted greyscale':
        line_color = invert_color(line_color)

    # INSIDE COLORING
    if asg_b == 'black':
        mid_color = csg.palette_style_guide['black']

    # CHECKING FOR CONFLICTS
    if asg_b == 'black':
        b_color = csg.palette_style_guide['black']
    elif asg_b == 'darkblue':
        b_color = csg.palette_style_guide['darkblue']
    elif asg_b == 'white':
        b_color = csg.palette_style_guide['white']
    else:
        raise ValueError("Incorrect background setup")

    if b_color == line_color:
        line_color = invert_color(line_color)

    line_pen = aggdraw.Pen(line_color, opt.single_line_width)
    mid_pen = aggdraw.Pen(mid_color, opt.double_line_inner_width)
    station_pen = aggdraw.Pen(line_color, opt.station_tick_width)

    # RENDERING
    if asg_b == 'darkblue':
        white_outline_pen = aggdraw.Pen(csg.palette_style_guide['white'], opt.single_line_width)
        line_pen = aggdraw.Pen(line_color, opt.night_tube_inline_width)
        for branch in line.branches:
            for geometry in branch.segment_list:
                if geometry is not None:
                    geometry.execute_render(draw, white_outline_pen)

    for branch in line.branches:
        for station in branch.station_list:
            if station is not None:
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

    return IMG