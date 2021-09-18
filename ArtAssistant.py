import random


def dist_calculator(num_art, art_types_n, art_types_p):
    art_order_dist = {}
    total = 0
    prob_absorber = None

    for art_type in art_types_n.keys():
        art_order_dist[art_type] = art_types_n[art_type]
        total += art_types_n[art_type]

    for art_type in art_types_p.keys():
        if art_types_p[art_type] == -1:
            if prob_absorber is not None:
                raise SystemExit("Error: More than one baseline probability type (-1) cannot be used")
            else:
                prob_absorber = art_type
        else:
            art_order_dist[art_type] = int(num_art * art_types_p[art_type])
            total += art_order_dist[art_type]

    art_order_dist[prob_absorber] = num_art - total
    if art_order_dist[prob_absorber] < 0:
        raise SystemExit("Error: Not enough total pieces of art to include n_type pieces")

    return art_order_dist


def order_randomizer(order_dist):
    order_list = []
    for art_type in order_dist.keys():
        order_list.extend([art_type] * order_dist[art_type])
    random.shuffle(order_list)
    return order_list
