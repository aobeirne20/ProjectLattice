import aggdraw
from PIL import ImageDraw

from map_lib.TMap import TMap
from map_lib.Line import Line
from color_lib.ColorOps import invert_color, greyscale_color

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg

def rLine(tmap: TMap, line: Line, IMG, art_style):
    draw = aggdraw.Draw(IMG)
    draw.setantialias(False)

    asg = csg.art_style_guide[art_style]
    lsg = line.style_details
    line_color = lsg['color']

    line_pen = aggdraw.Pen(line_color, opt.single_line_width)
    r, g, b, a = line_color
    # SOft transparent outline. Keep?
    #line_outline = aggdraw.Pen((r, g, b, 200), opt.single_line_width+(2*opt.s))
    white_mid_pen = aggdraw.Pen(csg.palette_style_guide['white'], opt.double_line_inner_width)

    for branch in line.branches:
        for frame in branch.frame_buffer:
            for station in frame.stations:
                station.execute_render(draw, line_pen)

    for branch in line.branches:
        for frame in branch.frame_buffer:
            if frame.geometry is not None:
                frame.geometry.execute_render(draw, line_pen)
                #frame.geometry.execute_render(draw, line_outline)

    if lsg['line_type'] == 'double':
        for branch in line.branches:
            for frame in branch.frame_buffer:
                if frame.geometry is not None:
                    frame.geometry.execute_render(draw, white_mid_pen)



    draw.flush()

    return IMG