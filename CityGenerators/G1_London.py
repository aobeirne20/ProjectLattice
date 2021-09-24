import Map
from MiscGenerators import GM1_LondonRiver
from LineGenerators import LG1_LondonNormal, LG1_LondonStations

import style_data


class G1_London:
    def __init__(self, size_tp):
        self.SD = style_data.StyleDatabase.London_style_guide
        self.xs = int(size_tp[0])
        self.ys = int(size_tp[1])
        self.map = Map.Map(self.xs, self.ys, style_data.StyleDatabase.t_scale)

        self.generate_primary_features()
        self.generate_lines()
        self.generate_stations()

    def generate_primary_features(self):
        # Features: River
        gen = GM1_LondonRiver.GM1_LondonRiver(self.xs, self.ys, self.map)
        self.map.primary_feature_list.append(Map.Line(name="LondonRiver", style=None, render_list=gen.generate(), station_list=None))
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
                print(f"-----------------------------------------------------------")
                print(line)
                render_list, stations = gen.outer_generate()

                self.map.line_list.append(Map.Line(name=line, style=self.SD[line], render_list=render_list, station_list=None))
                self.map.locus_list += stations

    def generate_stations(self):
        for line in self.map.line_list:
            gen = LG1_LondonStations.LG1_LondonStations(self.xs, self.ys, self.map)
            line.station_list = gen.generate_stations(line)

    def give_map(self):
        return self.map
