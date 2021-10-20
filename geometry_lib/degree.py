# 0 to 0, 1 to 45, 2 to 90, 3 to 135, 4 to 180, 5 to 225, 6 to 270, 7 to 315, 8!!! to 360!!!
import math


class degree(int):
    def __new__(cls, value, *args, **kwargs):
        value = value % 8
        if value < 0:
            value = 8 + value
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other: int):
        summ = super(degree, self).__add__(int(other))
        summ = summ % 8
        if summ < 0:
            summ = 8 + summ
        return self.__class__(summ)

    def __sub__(self, other: int):
        diff = super(degree, self).__sub__(int(other))
        diff = diff % 8
        if diff < 0:
            diff = 8 + diff
        return self.__class__(diff)

    @property
    def deg(self):
        return int(self * 45)

    @property
    def inv_deg(self):
        return int((8 - self) * 45)

    @property
    def rad(self):
        return float(self) * 0.25 * math.pi

    @property
    def ux(self):
        return math.cos(self.rad)

    @property
    def uy(self):
        return math.sin(self.rad)

    @property
    def change_to_0(self):
        move = -1*int(self)
        if move < -4:
            return 8 + move
        else:
            return move

    def vx(self, distance: int):
        return self.ux * distance

    def vy(self, distance: int):
        return self.uy * distance

    def __str__(self):
        return "%d" % int(self)

    def __repr__(self):
        return "positive(%d)" % int(self)




