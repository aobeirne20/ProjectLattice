import ArtDirector as AD

if __name__ == "__main__":
    director = AD.ArtDirector()
    director.calc_order_dist(art_order={"London": 20},

                              art_types_n={#"Anti-color": 1,
                                           "Night": 1,
                                           "Anti-night": 1,
                                           #"Dark": 1,
                                           "Anti-dark": 1,
                                           "Grey": 1,
                                           #"Anti-grey": 1,
                                           #"Dark Grey": 1,
                                           "Dark Anti-grey": 1,
                                           "Brightline": 1,
                                           #"Anti-brightline": 1,
                                           #"Darkline": 1,
                                           "Anti-brightline": 1,
                                           "Gold": 1,
                                           "Anti-gold": 1,
                                           "Dark Gold": 1,
                                           "Dark Anti-gold": 1,
                                           "Signature": 1},

                              art_types_p={"Color": -1})

    #director.create_gallery_structure()
    #director.i_am_a_creative_type()
    #director.i_sell_hotdogs(cities=["London"], art_type="Color")











