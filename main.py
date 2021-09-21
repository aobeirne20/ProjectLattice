import ArtDirector as AD

director = AD.ArtDirector()
director.calc_order_dist(art_order={"London": 1863, "Paris": 1900, "New York": 1904,
                                     "Moscow": 1935, "Tokyo": 1941, "Beijing": 1971},
                          art_types_n={"Signature": 1, "Gold": 10, "Anti_Gold": 5},
                          art_types_p={"Color": -1, "Anti_Color": 0.072, "Night": 0.24, "Anti_Night": 0.0288,
                                       "Brightline": 0.06, "Anti_Brightline": 0.0144,
                                        "Grey": 0.24, "Anti_Grey": 0.0288})
# director.create_gallery_structure()
director.i_sell_hotdogs(cities=["London"], art_type="Color")











