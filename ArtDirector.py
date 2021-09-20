import ArtAssistant as AA
import ImageGen as IG

import os
import json


class ArtDirector:
    def __init__(self):
        self.art_order = []
        self.batch_value = None

    def calc_order_dist(self, art_order, art_types_n, art_types_p):
        print(f"ORDER SUMMARY:")
        for city in art_order.keys():
            self.art_order.append({"City": city,
                                   "Order": AA.dist_calculator(art_order[city], art_types_n, art_types_p)})
            self.art_order[-1]["RList"] = AA.order_randomizer(self.art_order[-1]['Order'])
            sorted_order = {k: v for k, v in sorted(self.art_order[-1]["Order"].items(), key=lambda item: item[1])}
            print(f"{city}: {sorted_order}")
        print(f"")

    def create_gallery_structure(self):
        batch_value_txt = open("batch_value", 'r')
        self.batch_value = int(batch_value_txt.readline())
        batch_value_txt.close()
        batch_value_txt = open("batch_value", 'w')
        batch_value_txt.write(str(self.batch_value + 1))
        batch_value_txt.close()

        os.makedirs(f"Gallery/Batch_{self.batch_value:03d}/All")
        for city in self.art_order:
            os.makedirs(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/All")
            for art_type in city["Order"].keys():
                os.makedirs(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/{art_type}")

    def i_am_a_creative_type(self):
        num = 0
        for city in self.art_order:
            print(f"Starting generation for {city['City']}:")
            for art_type in city["RList"]:
                ig = IG.ImageGen(city=city, art_type=art_type)
                image, metadata = ig.ex_nihilo_res()
                image.save(f"Gallery/Batch_{self.batch_value:03d}/All/RapidTopology_{num:05d}", format=".png")
                image.save(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/All/RapidTopology_{num:05d}", format=".png")
                image.save(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/{art_type}RapidTopology_{num:05d}", format=".png")
                with open(f"Gallery/Batch_{self.batch_value:03d}/All/RapidTopology_{num:05d}.json", 'w') as outfile:
                    json.dump(metadata, outfile)
                with open(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/All/RapidTopology_{num:05d}.json", 'w') as outfile:
                    json.dump(metadata, outfile)
                with open(f"Gallery/Batch_{self.batch_value:03d}/{city['City']}/{art_type}RapidTopology_{num:05d}.json", 'w') as outfile:
                    json.dump(metadata, outfile)
                num += 1

    def i_sell_hotdogs(self, cities, art_type):
        num = 0
        for city in cities:
            print(f"Starting probability-blind generation for {city}:")
            ig = IG.ImageGen(city=city, art_type=art_type)
            image, metadata = ig.ex_nihilo_res()
            image.save(f"RapidTopology_{num:05d}.png")
            with open(f"RapidTopology_{num:05d}.json", 'w') as outfile:
                json.dump(metadata, outfile)
            num += 1

