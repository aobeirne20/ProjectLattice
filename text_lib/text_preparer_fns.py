import numpy as np

from options import prime as opt


def pools_preparer(import_pool: dict):
    primary_pools = {}
    backup_pool = []
    for pool in import_pool:
        current_names = import_pool[pool][0]
        expanded_names = import_pool[pool][1]
        alternate_names = import_pool[pool][2]

        backup_pool_addend = current_names + expanded_names

        if alternate_names:
            for n, name in enumerate(current_names):
                if alternate_names[n] is not None:
                    backup_pool_addend += alternate_names[n]
                    if np.random.choice([True, False], p=[opt.p_sub_name, 1-opt.p_sub_name]):
                        current_names[n] = np.random.choice(alternate_names[n])

        primary_pool = current_names + expanded_names

        np.random.shuffle(primary_pool)
        np.random.shuffle(backup_pool_addend)

        primary_pools[pool] = primary_pool
        backup_pool += backup_pool_addend

    return primary_pools, backup_pool


def spacing_preparer(station_name):
    spaced_names_list = []

    def space_recursor(phrase, location, built_phrase):
        if location == len(phrase):
            spaced_names_list.append(built_phrase)
            return

        if phrase[location] == ' ':
            space_recursor(phrase, location + 1, built_phrase + ' ')
            if phrase[location + 1] == '&':
                pass
            else:
                space_recursor(phrase, location + 1, built_phrase + '\n')
        else:
            space_recursor(phrase, location + 1, built_phrase + phrase[location])

    space_recursor(station_name, 0, '')
    return spaced_names_list
