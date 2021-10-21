def rgb8bit_to_dec(val):
    return val / 255


def srgb_to_lin(val):
    if val <= 0.04045:
        return val / 12.92
    else:
        return ((val + 0.055) / 1.055) ** 2.4


def lin_to_y(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def percieved_y_to_l(y):
    if y <= 216 / 24389:
        return y * 24389 / 27
    else:
        return (y ** (1 / 3)) * 116 - 16


def l_to_rgbu(l, a):
    k = (int(l/100*255), int(l/100*255), int(l/100*255), a)
    return k
