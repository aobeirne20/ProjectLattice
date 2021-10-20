from map_lib.TMap import TMap
from London.generate_lib import gRiver

class Generator:
    def __init__(self, csg):
        self.map = TMap()
        self.csg = csg

    def generate(self):
        river = gRiver.gRiver(self.csg)
        self.map.feature_list.append(river)

    def return_map(self):
        return self.map
