import sys

from manager_lib import ArtDirector as AD
from options.art_order import art_order
from ipfs_lib import PinataHandler as PH

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    director = AD.ArtDirector()
    director.calc_order_dist(art_order=art_order)

    #director.create_gallery_structure()
    #director.i_am_a_creative_type()

    #pinata_handler = PH.PinataHandler()
    #pinata_handler.pin_files()
    director.i_sell_hotdogs(city="London", art_type="Color")

