from Maps import M1_London
from MiscGenerators import GM1_LondonRiver
from LineGenerators import LG1_LondonNormal

import style_data

class G1_London:
    def __init__(self, art_type, size_tp):
        self.art_type = art_type
        self.SD = style_data.StyleDatabase
        self.xs = int(size_tp[0])
        self.ys = int(size_tp[1])
        self.map = M1_London.Map(self.xs, self.ys)

        self.generate_primary_features()
        self.generate_lines()

    def generate_primary_features(self):
        # Features: River
        gen = GM1_LondonRiver.GM1_LondonRiver(self.xs, self.ys, self.map)
        self.map.primary_feature_list.append(M1_London.Line(name="LondonRiver",)
            {"name": "LondonRiver", "render_path": gen.generate()})

    def generate_lines(self):
        for line in self.SD.London_style_guide.keys():
            print(line)
            if self.SD.London_style_guide[line]['type'] == "cable":
                pass
            elif self.SD.London_style_guide[line]['type'] == "light":
                pass
            elif self.SD.London_style_guide[line]['type'] == "heavy":
                pass
            elif self.SD.London_style_guide[line]['type'] == "circle":
                pass
            elif self.SD.London_style_guide[line]['type'] == "shuttle":
                pass
            elif self.SD.London_style_guide[line]['type'] == "normal":
                gen = LG1_LondonNormal.LG1_LondonNormal(self.xs, self.ys, self.map)
                self.map.line_list.append({"name": line, "render_path": gen.generate()})

    def give_map(self):
        return self.map
