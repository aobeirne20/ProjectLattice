import Map
from MiscGenerators import GM1_LondonRiver
from LineGenerators import LG1_LondonNormal, LG1_LondonStations, LG1_LondonInterchanges
from MiscRenderers import RM3_LondonTextPreparer
import random

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
        shuffled_keys = (list(self.SD.keys()))
        random.shuffle(shuffled_keys)
        for line in shuffled_keys:
            if self.SD[line]['gen_type'] == "secant":
                gen = LG1_LondonNormal.LG1_LondonNormal(self.xs, self.ys, self.map, line)
                print(f"-----------------------------------------------------------")
                print(line)
                render_list, stations = gen.outer_generate()

                self.map.line_list.append(Map.Line(name=line, style=self.SD[line], render_list=render_list, station_list=None))
                self.map.locus_list += stations
            elif self.SD[line]['gen_type'] == "circle":
                pass
            elif self.SD[line]['gen_type'] == "light":
                pass
            elif self.SD[line]['gen_type'] == "heavy":
                pass
            elif self.SD[line]['gen_type'] == "shuttle":
                pass
            elif self.SD[line]['gen_type'] == "tram":
                pass
            elif self.SD[line]['gen_type'] == "crossrail":
                pass
            else:
                print(f"This gen type does not exist")


    def generate_stations(self):
        text_giver = RM3_LondonTextPreparer.RM3_LondonTextPreparer()
        gen = LG1_LondonInterchanges.LG1_LondonInterchanges(self.xs, self.ys, self.map, text_giver)
        stations = gen.generate_stations()
        self.map.text_list = stations
        for line in self.map.line_list:
            gen = LG1_LondonStations.LG1_LondonStations(self.xs, self.ys, self.map, text_giver)
            temp = gen.generate_stations(line)
            self.map.text_list += temp
            line.station_list = temp

    def give_map(self):
        return self.map
