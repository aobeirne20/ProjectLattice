import os
import json
import time

from manager_lib import ArtAssistant as AA
import ImageGen as IG
from ipfs_lib import PinataHandler as PH

from parameters.StyleGuides import complete_style_guide as csg
from options import prime as opt


class ArtDirector:
    def __init__(self):
        self.art_order = None
        self.batch_value = None
        self.metadata = []
        print(f"\nInitializing Project Lattice, Renewed_v1")
        print(f"------------------------------------------------------------------------------------------------------------------------------------")

    def calc_order_dist(self, art_order):
        print(f"ORDER SUMMARY:\n")
        art_order_dist = AA.dist_calculator(art_order["num_pieces"], art_order["art_types_n"], art_order["art_types_p"])
        art_order_list = AA.order_lister_and_randomizer(art_order_dist)
        self.art_order = {"City": art_order["city"], "RList": art_order_list, "OrderDist": art_order_dist}

        sorted_order = {k: v for k, v in sorted(art_order_dist.items(), key=lambda item: item[1])}
        print(f"{self.art_order['City']}, {art_order['num_pieces']} pieces: \n{sorted_order}")
        print(f"\nValidating total piece count...")
        if art_order['num_pieces'] != len(self.art_order["RList"]):
            raise ValueError("Probability distribution has failed")
        else:
            print(f"{art_order['num_pieces']} pieces ordered, {len(self.art_order['RList'])} piece commands found")
            print(f"Successfully validated total piece count.\n")
        print(f"Validating options and CSG file...")
        if art_order['city'] != csg.csg_file_name or art_order['city'] != opt.options_file_name:
            raise ValueError("Wrong option and/or CSG file cold-swapped")
        else:
            print(f"Options and CSG files successfully validated!\n")
        print(f"Generating {csg.x}x{csg.y} output images(s), from a {csg.xs}x{csg.ys} super-sampler\n")

    def create_gallery_structure(self):
        batch_value_txt = open("options/value_counters/batch_value", 'r')
        self.batch_value = int(batch_value_txt.readline())
        batch_value_txt.close()
        batch_value_txt = open("options/value_counters/batch_value", 'w')
        batch_value_txt.write(str(self.batch_value + 1))
        batch_value_txt.close()

        os.makedirs(f"Gallery/Batch_{self.batch_value:03d}/All")
        for art_type in self.art_order["OrderDist"].keys():
            os.makedirs(f"Gallery/Batch_{self.batch_value:03d}/{art_type}")
        print(f"Created Gallery file structure for Batch {self.batch_value:03d} \n")

        for f in os.listdir('Scratch/IMG'):
            os.remove(os.path.join('Scratch/IMG', f))
        for f in os.listdir('Scratch/JSON'):
            os.remove(os.path.join('Scratch/JSON', f))

    def i_am_a_creative_type(self):
        num = 1
        gen_track = []
        print(f"Starting generation for {self.art_order['City']}:")
        for art_type in self.art_order["RList"]:
            time_start = time.perf_counter()
            ig = IG.ImageGen(city=self.art_order['City'], art_style=art_type)
            image, metadata = ig.ex_nihilo_res()
            self.metadata.append([metadata, num])
            image.save(f"Scratch/IMG/{num}.png")
            image.save(f"Gallery/Batch_{self.batch_value:03d}/All/{num}_{art_type}.png")
            image.save(f"Gallery/Batch_{self.batch_value:03d}/{art_type}/{num}.png")
            time_end = time.perf_counter()

            # Loading Bar
            gen_track.append(time_end - time_start)
            bar = u'\u2588'
            n_blocks = int(num * 50 / len(self.art_order["RList"]))
            time_remaining = (sum(gen_track)/len(gen_track)) * (len(self.art_order["RList"])-num)
            m, s = divmod(time_remaining, 60)
            h, m = divmod(m, 60)
            print(f'\rPiece {num:04d}/{len(self.art_order["RList"]):04d} |{bar * n_blocks}{" " * (50 - n_blocks)}|  '
                  f'Estimated Time Remaining: {h:.0f}h{m:.0f}m{s:.0f}s', end='')

            # Increment the counter
            num += 1

    def pin_to_ipfs(self):
        pinata_handler = PH.PinataHandler()
        img_directory_cid = pinata_handler.pin_files()

        for metadata in self.metadata:
            metadata[0]["name"] = self.art_order["City"] + " #" + str(metadata[1])
            metadata[0]["image"] = "ipfs://" + img_directory_cid + "/" + str(metadata[1]) + ".png"
            metadata[0]["external_url"] = "metrotopology.mypinata.cloud/ipfs/" + img_directory_cid + "/" + str(metadata[1]) + ".png"

            with open(f'Scratch/JSON/{str(metadata[1])}.json', 'w') as outfile:
                json.dump(metadata, outfile)

        json_directory_cid = pinata_handler.pin_json()
        final_url = "metrotopology.mypinata.cloud/ipfs/" + json_directory_cid
        print(f"\n{final_url}")

    def i_sell_hotdogs(self, city, art_type):
        scratch_value_txt = open("options/value_counters/scratch_value", 'r')
        scratch_value = int(scratch_value_txt.readline())
        scratch_value_txt.close()
        scratch_value_txt = open("options/value_counters/scratch_value", 'w')
        scratch_value_txt.write(str(scratch_value + 1))
        scratch_value_txt.close()

        print(f"Bypassing probability generation and file structure, generating one {art_type} of {city}:")
        ig = IG.ImageGen(city=city, art_style=art_type)
        image, metadata = ig.ex_nihilo_res()
        print(metadata)
        image.show()
        image.save(f"Gallery/Hotdogs/MetroTopology_{scratch_value}_{city}_{art_type}.png")




