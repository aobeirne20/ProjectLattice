import Map
from MiscGenerators import GM1_LondonRiver
from LineGenerators import LG1_LondonNormal

import style_data


class G1_London:
    def __init__(self, size_tp):
        self.SD = style_data.StyleDatabase.London_style_guide
        self.xs = int(size_tp[0])
        self.ys = int(size_tp[1])
        self.map = Map.Map(self.xs, self.ys, style_data.StyleDatabase.t_scale)

        self.generate_primary_features()
        self.generate_lines()

    def generate_primary_features(self):
        # Features: River
        gen = GM1_LondonRiver.GM1_LondonRiver(self.xs, self.ys, self.map)
        self.map.primary_feature_list.append(Map.Line(name="LondonRiver", style=None, render_list=gen.generate()))
        # Primary features complete

    def generate_lines(self):
        for line in self.SD.keys():
            if self.SD[line]['type'] == "cable":
                pass
            elif self.SD[line]['type'] == "light":
                pass
            elif self.SD[line]['type'] == "heavy":
                pass
            elif self.SD[line]['type'] == "circle":
                pass
            elif self.SD[line]['type'] == "shuttle":
                pass
            elif self.SD[line]['type'] == "normal":
                gen = LG1_LondonNormal.LG1_LondonNormal(self.xs, self.ys, self.map)
                print(line)
                self.map.line_list.append(Map.Line(name=line, style=self.SD[line], render_list=gen.outer_generate()))

    def give_map(self):
        return self.map
