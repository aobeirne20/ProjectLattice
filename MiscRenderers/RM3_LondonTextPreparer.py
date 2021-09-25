import geometric_elements as ge
import aggdraw
import math
import random as r
import numpy as np

import PIL
from PIL import Image
import style_data as sd
import names_london as names

class RM3_LondonTextPreparer():
    def __init__(self):
        # INGEST TEXT
        pool_dict = {'crossrail': names.crossrail_names, 'overground': names.overground_names,
                        'tram': names.tram_names, 'dlr': names.dlr_names, 'underground': names.underground_names}

        pool_lists = []
        backup_pool = []
        for pool in pool_dict:
            name_list = pool_dict[pool]
            primary_list = name_list[0]
            alternate_list = name_list[1]
            substitute_list = name_list[2]
            shuffled_list = []

            backup_pool += alternate_list
            backup_pool += substitute_list

            r.shuffle(primary_list)
            for num, name in enumerate(primary_list):
                if substitute_list:
                    if substitute_list[num] is not None:
                        if np.random.choice([True, False], p=[0.1, 0.9]):
                            sub_name = np.random.choice(substitute_list[num])
                            shuffled_list.append(sub_name)
                            continue
                if alternate_list and np.random.choice([True, False], p=[0.2, 0.8]):
                    shuffled_list.append(alternate_list.pop())
                shuffled_list.append(primary_list[num])
            pool_lists.append(shuffled_list)

        self.pools_list = pool_lists
        self.backup_pool = backup_pool
        self.used_list = []


    def give_name(self, name_pool):
        if name_pool == 'crossrail':
            pool_code = 0
        elif name_pool == 'overground':
            pool_code = 1
        elif name_pool == 'tram':
            pool_code = 2
        elif name_pool == 'dlr':
            pool_code = 3
        elif name_pool == 'underground' or name_pool == 'normal':
            pool_code = 4
        else:
            print(f"This name pool does not exist.")
            pool_code = 4

        while True:
            if self.pools_list[pool_code] is False:
                name = self.backup_pool.pop()
            else:
                name = self.pools_list[pool_code].pop()

            if self.used_list.count(name) > 0:
                continue
            else:
                self.used_list.append(name)
                return name
