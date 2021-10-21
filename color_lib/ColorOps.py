from color_lib.ColorHelpers import *


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


