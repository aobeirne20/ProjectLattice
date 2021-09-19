import aggdraw
import math


class Segment:
    def __init__(self, style, loc1, loc2, orientation):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.style = style

    def render(self, draw, scale):
        pass

    def render_specific(self, pen, draw, scale):
        draw.line((self.loc1[0] * scale, self.loc1[1] * scale,
                   self.loc2[0] * scale, self.loc2[1] * scale), pen)


class Arc90:
    def __init__(self, style, loc1, orientation, chirality):
        self.style = style

        if chirality == 'R':
            if orientation == 0:
                center = (loc1[0], loc1[1] + 1)
            elif orientation == 90:
                center = (loc1[0] + 1, loc1[1])
            elif orientation == 180:
                center = (loc1[0], loc1[1] - 1)
            elif orientation == 270:
                center = (loc1[0] - 1, loc1[1])
            self.start_d = orientation
            self.end_d = orientation + 90

        elif chirality == 'L':
            if orientation == 0:
                center = (loc1[0], loc1[1] - 1)
            elif orientation == 90:
                center = (loc1[0] - 1, loc1[1])
            elif orientation == 180:
                center = (loc1[0], loc1[1] + 1)
            elif orientation == 270:
                center = (loc1[0] + 1, loc1[1])
            self.start_d = orientation - 90
            self.end_d = orientation

        self.upper_l = (center[0] - 1, center[1] - 1)
        self.bottom_r = (center[0] + 1, center[1] + 1)

    def render_specific(self, pen, draw, scale):
        draw.arc((self.upper_l[0] * scale, self.upper_l[1] * scale, self.bottom_r[0] * scale, self.bottom_r[1] * scale),
                 self.start_d - 2, self.end_d + 2, pen)


class Arc45:
    def __init__(self, style, loc1, loc2, orientation, chirality):
        self.loc1 = loc1
        self.loc2 = loc2
        self.orientation = orientation
        self.chirality = chirality
        self.style = style

        self.intro_seg = None
        self.outro_seg = None
        self.arc = None

        # INTRO SEG
        if chirality == 'Rs' or chirality == 'Ls':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + (2 - 2*math.sqrt(0.5)), loc1[1])
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0], loc1[1] - (2 - 2*math.sqrt(0.5)))
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - (2 - 2*math.sqrt(0.5)), loc1[1])
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0], loc1[1] + (2 - 2*math.sqrt(0.5)))
        if chirality == 'Rd':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + math.sqrt(0.5), loc1[1] + math.sqrt(0.5))
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + math.sqrt(0.5), loc1[1] - math.sqrt(0.5))
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - math.sqrt(0.5), loc1[1] - math.sqrt(0.5))
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - math.sqrt(0.5), loc1[1] + math.sqrt(0.5))
        if chirality == 'Ld':
            if orientation == 0:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + math.sqrt(0.5), loc1[1] - math.sqrt(0.5))
            elif orientation == 90:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - math.sqrt(0.5), loc1[1] - math.sqrt(0.5))
            elif orientation == 180:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] - math.sqrt(0.5), loc1[1] + math.sqrt(0.5))
            elif orientation == 270:
                self.intro_seg = (loc1[0], loc1[1], loc1[0] + math.sqrt(0.5), loc1[1] + math.sqrt(0.5))

        # OUTRO SEG
        if chirality == 'Rd':
            if orientation == 0:
                self.outro_seg = (loc2[0], loc2[1] - (2 - 2*math.sqrt(0.5)), loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] - (2 - 2*math.sqrt(0.5)), loc2[1], loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0], loc2[1] + (2 - 2*math.sqrt(0.5)), loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] + (2 - 2*math.sqrt(0.5)), loc2[1], loc2[0], loc2[1])
        if chirality == 'Ld':
            if orientation == 0:
                self.outro_seg = (loc2[0], loc2[1] + (2 - 2*math.sqrt(0.5)), loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] + (2 - 2*math.sqrt(0.5)), loc2[1], loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0], loc2[1] - (2 - 2*math.sqrt(0.5)), loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] - (2 - 2*math.sqrt(0.5)), loc2[1], loc2[0], loc2[1])
        if chirality == 'Rs':
            if orientation == 0:
                self.outro_seg = (loc2[0] - math.sqrt(0.5), loc2[1] - math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] - math.sqrt(0.5), loc2[1] + math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0] + math.sqrt(0.5), loc2[1] + math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] + math.sqrt(0.5), loc2[1] - math.sqrt(0.5), loc2[0], loc2[1])
        if chirality == 'Ls':
            if orientation == 0:
                self.outro_seg = (loc2[0] - math.sqrt(0.5), loc2[1] + math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 90:
                self.outro_seg = (loc2[0] + math.sqrt(0.5), loc2[1] + math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 180:
                self.outro_seg = (loc2[0] + math.sqrt(0.5), loc2[1] - math.sqrt(0.5), loc2[0], loc2[1])
            elif orientation == 270:
                self.outro_seg = (loc2[0] - math.sqrt(0.5), loc2[1] - math.sqrt(0.5), loc2[0], loc2[1])

        # ARC
        if chirality == 'Rs':
            if orientation == 0:
                center = (self.intro_seg[2], self.intro_seg[3] + 1)
            elif orientation == 90:
                center = (self.intro_seg[2] + 1, self.intro_seg[3])
            elif orientation == 180:
                center = (self.intro_seg[2], self.intro_seg[3] - 1)
            elif orientation == 270:
                center = (self.intro_seg[2] - 1, self.intro_seg[3])
            self.start_d = orientation + 45
            self.end_d = orientation + 90

        elif chirality == 'Ls':
            if orientation == 0:
                center = (self.intro_seg[2], self.intro_seg[3] - 1)
            elif orientation == 90:
                center = (self.intro_seg[2] - 1, self.intro_seg[3])
            elif orientation == 180:
                center = (self.intro_seg[2], self.intro_seg[3] + 1)
            elif orientation == 270:
                center = (self.intro_seg[2] + 1, self.intro_seg[3])
            self.start_d = orientation - 90
            self.end_d = orientation - 45

        elif chirality == 'Rd':
            if orientation == 0:
                center = (self.outro_seg[0] - 1, self.outro_seg[1])
            elif orientation == 90:
                center = (self.outro_seg[0], self.outro_seg[1] + 1)
            elif orientation == 180:
                center = (self.outro_seg[0] + 1, self.outro_seg[1])
            elif orientation == 270:
                center = (self.outro_seg[0], self.outro_seg[1] - 1)
            self.start_d = orientation
            self.end_d = orientation + 45

        elif chirality == 'Ld':
            if orientation == 0:
                center = (self.outro_seg[0] - 1, self.outro_seg[1])
            elif orientation == 90:
                center = (self.outro_seg[0], self.outro_seg[1] + 1)
            elif orientation == 180:
                center = (self.outro_seg[0] + 1, self.outro_seg[1])
            elif orientation == 270:
                center = (self.outro_seg[0], self.outro_seg[1] - 1)
            self.start_d = orientation - 45
            self.end_d = orientation

        self.upper_l = (center[0] - 1, center[1] - 1)
        self.bottom_r = (center[0] + 1, center[1] + 1)


    def render_specific(self, pen, draw, scale):
        draw.arc((self.upper_l[0] * scale, self.upper_l[1] * scale, self.bottom_r[0] * scale, self.bottom_r[1] * scale),
                 self.start_d - 3, self.end_d + 3, pen)
        draw.line((self.intro_seg[0] * scale, self.intro_seg[1] * scale,
                   self.intro_seg[2] * scale, self.intro_seg[3] * scale), pen)
        draw.line((self.outro_seg[0] * scale, self.outro_seg[1] * scale,
                   self.outro_seg[2] * scale, self.outro_seg[3] * scale), pen)








