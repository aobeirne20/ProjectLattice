import numpy as np

from map_lib.TMap import TMap
from London.generate_lib import gRiver
from London.generate_lib.line import gLineSecant
from London.generate_lib import interchange

from parameters.StyleGuides import complete_style_guide as csg


class Generator:
    def __init__(self):
        self.map = TMap()

    def generate(self):
        # RIVER
        river = gRiver.gRiver()
        self.map.feature_list.append(river)

        # LINE PRE-PROCESSING
        gen_cycles = 0
        gen_list = []
        for line in csg.line_style_guide.values():
            gen_cycles = max(gen_cycles, line['gen_order'])
        for cycle in range(0, gen_cycles+1):
            gen_list.append([])
        for line in csg.line_style_guide.values():
            gen_list[line['gen_order']].append(line)

        for cycle in gen_list:
            np.random.shuffle(cycle)
            for line in cycle:
                if line['gen_type'] == 'secant':
                    gennie = gLineSecant.gLineSecant(self.map, line)
                    self.map.line_list.append(gennie.return_line())

        self.map.combine_interchanges()



    def return_map(self):
        return self.map
