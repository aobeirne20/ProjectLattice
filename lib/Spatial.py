from lib.degree import degree


class Spatial:
    def __init__(self, x: int, y: int, o: degree):
        self.x = x
        self.y = y
        self.o = o

    def vx(self, distance: int):
        return self.o.ux * distance

    def vy(self, distance: int):
        return self.o.uy * distance

    @property
    def t(self):
        t = (self.x, self.y)
        return t

