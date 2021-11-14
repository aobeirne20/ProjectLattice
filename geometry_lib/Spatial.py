from geometry_lib.degree import degree


class Spatial:
    def __init__(self, x: int, y: int, o: degree):
        self.x = x
        self.y = y
        self.o = o

    @property
    def t(self):
        t = (self.x, self.y)
        return t

    def is_same_location(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return f"({self.x}, {self.y}) @ {self.o} [{self.o.deg}°]"

