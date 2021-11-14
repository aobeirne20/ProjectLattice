from London.generate_lib import G1_London, T1_London
from London.render_lib import R1_London
from London.metadata_lib import M1_London


class CompleteMaterializer:
    def __init__(self, city, art_style):
        if city == 'London':
            self.generator = G1_London.Generator(T1_London.Texterator())
            self.renderer = R1_London.Renderer(art_style=art_style)
            self.metadata = M1_London.Metadata()