from map_lib.TMap import TMap
from London.generate_lib import gRiver


class Generator:
    def __init__(self):
        self.map = TMap()

    def generate(self):
        # RIVER
        river = gRiver.gRiver()
        self.map.feature_list.append(river)

        # LINES: SECANTS

    def return_map(self):
        return self.map
