from color_lib.ColorHelpers import *

from parameters.StyleGuides import complete_style_guide as csg

def invert_color(rgba_color):
    inverted_color = [255 - dcode for dcode in rgba_color]
    inverted_color[-1] = rgba_color[-1]
    return tuple(inverted_color)


def greyscale_color(rgba_color):
    rgb8 = rgba_color[0:3]
    rgb_dec = [rgb8bit_to_dec(n) for n in rgb8]
    r, g, b = [srgb_to_lin(n) for n in rgb_dec]
    y = lin_to_y(r, g, b)
    l = percieved_y_to_l(y)
    k = l_to_rgbu(l, rgba_color[-1])
    return k


def goldshade_color(rgba_color):
    greyed = greyscale_color(rgba_color)
    r, g, b, a = greyed
    r0, g0, b0, a0 = csg.palette_style_guide['gold_stop']
    r1, g1, b1, a1 = csg.palette_style_guide['gold_start']
    r_gold = int((r / 255) * (r1 - r0) + r0)
    g_gold = int((g / 255) * (g1 - g0) + g0)
    b_gold = int((b / 255) * (b1 - b0) + b0)
    return tuple([r_gold, g_gold, b_gold, a])




