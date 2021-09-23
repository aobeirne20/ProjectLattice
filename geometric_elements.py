import math


class Segment:
    def __init__(self, loc1, loc2, orientation):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.sandwich_R = None
        self.sandwich_L = None

    def render(self, pen, draw):
        draw.line((self.loc1[0], self.loc1[1],
                   self.loc2[0], self.loc2[1]), pen)


def arc_builder(arc_type, loc1, loc2, orientation, chirality, curve_scale):
    if arc_type == 45:
        return Arc45(loc1, loc2, orientation, chirality, curve_scale)
    if arc_type == 90:
        return Arc90(loc1, loc2, orientation, chirality, curve_scale)


class EndCap:
    def __init__(self, loc1, loc2, orientation):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.sandwich_R = None
        self.sandwich_L = None

    def render(self, pen, draw):
        draw.line((self.loc1[0], self.loc1[1],
                   self.loc2[0], self.loc2[1]), pen)


class Arc90:
    def __init__(self, loc1, loc2, orientation, chirality, curve_scale):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.center = None
        self.sandwich_R = None
        self.sandwich_L = None
        self.curve_scale = curve_scale
        self.chirality = chirality

        if chirality == 'R':
            if orientation == 0:
                center = (loc1[0], loc1[1] + curve_scale)
            elif orientation == 90:
                center = (loc1[0] + curve_scale, loc1[1])
            elif orientation == 180:
                center = (loc1[0], loc1[1] - curve_scale)
            elif orientation == 270:
                center = (loc1[0] - curve_scale, loc1[1])
            self.start_d = orientation
            self.end_d = orientation + 90

        elif chirality == 'L':
            if orientation == 0:
                center = (loc1[0], loc1[1] - curve_scale)
            elif orientation == 90:
                center = (loc1[0] - curve_scale, loc1[1])
            elif orientation == 180:
                center = (loc1[0], loc1[1] + curve_scale)
            elif orientation == 270:
                center = (loc1[0] + curve_scale, loc1[1])
            self.start_d = orientation - 90
            self.end_d = orientation

        self.upper_l = (center[0] - curve_scale, center[1] - curve_scale)
        self.bottom_r = (center[0] + curve_scale, center[1] + curve_scale)
        self.center = center

    def render(self, pen, draw):
        draw.arc((self.upper_l[0], self.upper_l[1], self.bottom_r[0], self.bottom_r[1]),
                 self.start_d - 2, self.end_d + 2, pen)


class Arc45:
    def __init__(self, loc1, loc2, orientation, chirality, curve_scale):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.chirality = chirality
        self.center = None
        self.sandwich_R = None
        self.sandwich_L = None

        self.intro_seg = None
        self.outro_seg = None
        self.arc = None
        self.curve_scale = curve_scale

        strt = (2 - 2*math.sqrt(0.5)) * curve_scale
        diag = math.sqrt(0.5) * curve_scale

        # INTRO SEG
        if chirality == 'Rs' or chirality == 'Ls':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + strt, loc1[1])
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0], loc1[1] - strt)
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - strt, loc1[1])
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0], loc1[1] + strt)
        if chirality == 'Rd':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + diag, loc1[1] + diag)
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + diag, loc1[1] - diag)
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - diag, loc1[1] - diag)
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - diag, loc1[1] + diag)
        if chirality == 'Ld':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + diag, loc1[1] - diag)
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - diag, loc1[1] - diag)
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - diag, loc1[1] + diag)
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + diag, loc1[1] + diag)

        # OUTRO SEG
        if chirality == 'Rd':
            if orientation == 0:
                self.outro_seg = (loc2[0], loc2[1] - strt, loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] - strt, loc2[1], loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0], loc2[1] + strt, loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] + strt, loc2[1], loc2[0], loc2[1])
        if chirality == 'Ld':
            if orientation == 0:
                self.outro_seg = (loc2[0], loc2[1] + strt, loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] + strt, loc2[1], loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0], loc2[1] - strt, loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] - strt, loc2[1], loc2[0], loc2[1])
        if chirality == 'Rs':
            if orientation == 0:
                self.outro_seg = (loc2[0] - diag, loc2[1] - diag, loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] - diag, loc2[1] + diag, loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0] + diag, loc2[1] + diag, loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] + diag, loc2[1] - diag, loc2[0], loc2[1])
        if chirality == 'Ls':
            if orientation == 0:
                self.outro_seg = (loc2[0] - diag, loc2[1] + diag, loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] + diag, loc2[1] + diag, loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0] + diag, loc2[1] - diag, loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] - diag, loc2[1] - diag, loc2[0], loc2[1])

        # ARC
        if chirality == 'Rs':
            if orientation == 0:
                center = (self.intro_seg[2], self.intro_seg[3] + curve_scale)
            elif orientation == 90:
                center = (self.intro_seg[2] + curve_scale, self.intro_seg[3])
            elif orientation == 180:
                center = (self.intro_seg[2], self.intro_seg[3] - curve_scale)
            elif orientation == 270:
                center = (self.intro_seg[2] - curve_scale, self.intro_seg[3])
            self.start_d = orientation + 45
            self.end_d = orientation + 90

        elif chirality == 'Ls':
            if orientation == 0:
                center = (self.intro_seg[2], self.intro_seg[3] - curve_scale)
            elif orientation == 90:
                center = (self.intro_seg[2] - curve_scale, self.intro_seg[3])
            elif orientation == 180:
                center = (self.intro_seg[2], self.intro_seg[3] + curve_scale)
            elif orientation == 270:
                center = (self.intro_seg[2] + curve_scale, self.intro_seg[3])
            self.start_d = orientation - 90
            self.end_d = orientation - 45

        elif chirality == 'Rd':
            if orientation == 0:
                center = (self.outro_seg[0] - curve_scale, self.outro_seg[1])
            elif orientation == 90:
                center = (self.outro_seg[0], self.outro_seg[1] + curve_scale)
            elif orientation == 180:
                center = (self.outro_seg[0] + curve_scale, self.outro_seg[1])
            elif orientation == 270:
                center = (self.outro_seg[0], self.outro_seg[1] - curve_scale)
            self.start_d = orientation
            self.end_d = orientation + 45

        elif chirality == 'Ld':
            if orientation == 0:
                center = (self.outro_seg[0] - curve_scale, self.outro_seg[1])
            elif orientation == 90:
                center = (self.outro_seg[0], self.outro_seg[1] + curve_scale)
            elif orientation == 180:
                center = (self.outro_seg[0] + curve_scale, self.outro_seg[1])
            elif orientation == 270:
                center = (self.outro_seg[0], self.outro_seg[1] - curve_scale)
            self.start_d = orientation - 45
            self.end_d = orientation

        self.upper_l = (center[0] - curve_scale, center[1] - curve_scale)
        self.bottom_r = (center[0] + curve_scale, center[1] + curve_scale)
        self.center = center

    def render(self, pen, draw):
        draw.arc((self.upper_l[0], self.upper_l[1], self.bottom_r[0], self.bottom_r[1]),
                 self.start_d - 3, self.end_d + 3, pen)
        draw.line((self.intro_seg[0], self.intro_seg[1],
                   self.intro_seg[2], self.intro_seg[3]), pen)
        draw.line((self.outro_seg[0], self.outro_seg[1],
                   self.outro_seg[2], self.outro_seg[3]), pen)








