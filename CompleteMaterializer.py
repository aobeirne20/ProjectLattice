from London.generate_lib import G1_London
from London.render_lib import R1_London


class CompleteMaterializer:
    def __init__(self, city, csg):
        if city == 'London':
            self.generator = G1_London.Generator(csg)
            self.renderer = R1_London.Renderer(csg)