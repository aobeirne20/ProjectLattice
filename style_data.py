
class StyleDatabase:
    map_style_guide = {
        "London": {
             "x_size": 6000,
             "y_size": 4000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)},
         "Paris": {
             "x_size": 6000,
             "y_size": 6000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)},
         "New York": {
             "x_size": 5000,
             "y_size": 6000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)},
         "Moscow": {
             "x_size": 5000,
             "y_size": 6000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)},
         "Tokyo": {
             "x_size": 6000,
             "y_size": 4000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)},
         "Beijing": {
             "x_size": 6000,
             "y_size": 4000,
             "default_background": (255, 255, 255, 255),
             "dark_background": (0, 0, 0, 255)}

        }


    London_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # LONDON
        "Emirates Air": {
            "city": "London",
            "color": (220, 36, 31, 255),
            "type": "cable",
            "style": "double"},
        "DLR": {
            "city": "London",
            "color": (0, 175, 173, 255),
            "type": "light",
            "style": "double"},
        "Overground": {
             "city": "London",
             "color": (239, 123, 16, 255),
             "type": "heavy",
             "style": "double"},
        "London Tram": {
             "city": "London",
             "color": (0, 189, 25, 255),
             "type": "heavy",
             "style": "double"},
        "Elizabeth": {
             "city": "London",
             "color": (147, 100, 204, 255),
             "type": "normal",
             "style": "double"},

        "Bakerloo": {
             "city": "London",
             "color": (178, 99, 0, 255),
             "type": "normal",
             "style": "single"},
        "Central": {
             "city": "London",
             "color": (220, 36, 31, 255),
             "type": "normal",
             "style": "single"},
        "Circle": {
             "city": "London",
             "color": (255, 211, 41, 255),
             "type": "circle",
             "style": "single"},
        "District": {
             "city": "London",
             "color": (0, 125, 50, 255),
             "type": "normal",
             "style": "single"},
        "H'Smith & City": {
             "city": "London",
             "color": (244, 169, 190, 255),
             "type": "normal",
             "style": "single"},
        "Jubilee": {
             "city": "London",
             "color": (161, 165, 167, 255),
             "type": "normal",
             "style": "single"},
        "Metropolitan": {
             "city": "London",
             "color": (155, 0, 88, 255),
             "type": "normal",
             "style": "single"},
        "Northern": {
             "city": "London",
             "color": (0, 0, 0, 255),
             "type": "normal",
             "style": "single"},
        "Picadilly": {
             "city": "London",
             "color": (0, 25, 168, 255),
             "type": "normal",
             "style": "single"},
        "Victoria": {
             "city": "London",
             "color": (0, 152, 216, 255),
             "type": "normal",
             "style": "single"},
        "Waterloo & City": {
             "city": "London",
             "color": (147, 206, 186, 255),
             "type": "shuttle",
             "style": "single"},
    }


    Paris_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # PARIS
        "1": {
             "city": "Paris",
             "color": (255, 206, 0, 255),
             "type": "normal",
             "style": "single"},
        "2": {
             "city": "Paris",
             "color": (0, 100, 176, 255),
             "type": "semi",
             "style": "single"},
        "3": {
             "city": "Paris",
             "color": (159, 152, 37, 255),
             "type": "normal",
             "style": "single"},
        "3bis": {
             "city": "Paris",
             "color": (152, 212, 226, 255),
             "type": "shuttle",
             "style": "single"},
        "4": {
             "city": "Paris",
             "color": (192, 65, 145, 255),
             "type": "normal",
             "style": "single"},
        "5": {
             "city": "Paris",
             "color": (242, 142, 66, 255),
             "type": "normal",
             "style": "single"},
        "6": {
             "city": "Paris",
             "color": (131, 196, 145, 255),
             "type": "semi",
             "style": "single"},
        "7": {
             "city": "Paris",
             "color": (243, 164, 186, 255),
             "type": "normal",
             "style": "single"},
        "7bis": {
             "city": "Paris",
             "color": (131, 196, 145, 255),
             "type": "shuttle",
             "style": "single"},
        "8": {
             "city": "Paris",
             "color": (206, 173, 210, 255),
             "type": "normal",
             "style": "single"},
        "9": {
             "city": "Paris",
             "color": (213, 201, 0, 255),
             "type": "normal",
             "style": "single"},
        "10": {
             "city": "Paris",
             "color": (227, 179, 42, 255),
             "type": "normal",
             "style": "single"},
        "11": {
             "city": "Paris",
             "color": (141, 94, 42, 255),
             "type": "normal",
             "style": "single"},
        "12": {
             "city": "Paris",
             "color": (0, 129, 79, 255),
             "type": "normal",
             "style": "single"},
        "13": {
             "city": "Paris",
             "color": (152, 212, 226, 255),
             "type": "normal",
             "style": "single"},
        "14": {
             "city": "Paris",
             "color": (102, 36, 131, 255),
             "type": "normal",
             "style": "single"},

        "A": {
             "city": "Paris",
             "color": (227, 5, 28, 255),
             "type": "heavy",
             "style": "single_thick"},
        "B": {
             "city": "Paris",
             "color": (82, 145, 206, 255),
             "type": "heavy",
             "style": "single_thick"},
        "C": {
             "city": "Paris",
             "color": (255, 206, 0, 255),
             "type": "heavy",
             "style": "single_thick"},
        "D": {
             "city": "Paris",
             "color": (0, 129, 79, 255),
             "type": "heavy",
             "style": "single_thick"},
        "E": {
             "city": "Paris",
             "color": (192, 65, 145, 255),
             "type": "heavy",
             "style": "single_thick"},

        "T1": {
             "city": "Paris",
             "color": (0, 100, 176, 255),
             "type": "tram",
             "style": "single_thin"},
        "T2": {
             "city": "Paris",
             "color": (192, 65, 145, 255),
             "type": "tram",
             "style": "single_thin"},
        "T3a": {
             "city": "Paris",
             "color": (242, 142, 66, 255),
             "type": "tram",
             "style": "single_thin"},
        "T3b": {
             "city": "Paris",
             "color": (0, 129, 79, 255),
             "type": "tram",
             "style": "single_thin"},
        "T4": {
             "city": "Paris",
             "color": (227, 179, 42, 255),
             "type": "tram",
             "style": "single_thin"},
        "T5": {
             "city": "Paris",
             "color": (102, 36, 131, 255),
             "type": "tram",
             "style": "single_thin"},
        "T6": {
             "city": "Paris",
             "color": (227, 5, 28, 255),
             "type": "tram",
             "style": "single_thin"},
        "T7": {
             "city": "Paris",
             "color": (141, 94, 42, 255),
             "type": "tram",
             "style": "single_thin"},
        "T8": {
             "city": "Paris",
             "color": (159, 152, 37, 255),
             "type": "tram",
             "style": "single_thin"},
        "T9": {
             "city": "Paris",
             "color": (82, 145, 206, 255),
             "type": "tram",
             "style": "single_thin"},
        "T11": {
             "city": "Paris",
             "color": (242, 142, 66, 255),
             "type": "tram",
             "style": "single_thin"},
    }


    NewYork_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # NEW YORK
        "IND Eighth Avenue": {
             "city": "New York",
             "color": (0, 57, 166, 255),
             "type": "normal",
             "style": "single",
             "special": ["A", "C", "E"]},
        "IND Sixth Avenue": {
             "city": "New York",
             "color": (255, 99, 25, 255),
             "type": "expressed",
             "style": "single",
             "special": ["B", "D", "F", "<F>", "M"]},
        "IND Crosstown": {
             "city": "New York",
             "color": (108, 190, 69, 255),
             "type": "normal",
             "style": "single",
             "special": ["G"]},
        "BMT Canarsie": {
             "city": "New York",
             "color": (167, 169, 172, 255),
             "type": "normal",
             "style": "single",
             "special": ["L"]},
        "BMT Nassau Street": {
             "city": "New York",
             "color": (153, 102, 51, 255),
             "type": "normal",
             "style": "single",
             "special": ["J", "Z"]},
        "BMT Broadway": {
             "city": "New York",
             "color": (252, 204, 10, 255),
             "type": "normal",
             "style": "single",
             "special": ["N", "Q", "R", "W"]},
        "IRT Broadway-Seventh Avenue": {
             "city": "New York",
             "color": (238, 53, 46, 255),
             "type": "normal",
             "style": "single",
             "special": ["1", "2", "3"]},
        "IRT Lexington": {
             "city": "New York",
             "color": (0, 147, 60, 255),
             "type": "expressed",
             "style": "single",
             "special": ["4", "5", "6", "<6>"]},
        "IRT Flushing": {
             "city": "New York",
             "color": (185, 51, 173, 255),
             "type": "expressed",
             "style": "single",
             "special": ["7", "<7>"]},
        "42nd Street Shuttle": {
             "city": "New York",
             "color": (128, 129, 131, 255),
             "type": "shuttle",
             "style": "single",
             "special": ["S"]},
        "Rockaway Park Shuttle": {
             "city": "New York",
             "color": (128, 129, 131, 255),
             "type": "shuttle",
             "style": "single",
             "special": ["SR"]},
        "Franklin Avenue Shuttle": {
             "city": "New York",
             "color": (128, 129, 131, 255),
             "type": "shuttle",
             "style": "single",
             "special": ["SF"]},
        "Staten Island Railroad": {
             "city": "New York",
             "color": (7, 106, 174, 255),
             "type": "island",
             "style": "single",
             "special": ["SIR"]},

        "Airtrain JFK": {
             "city": "New York",
             "color": (249, 238, 6, 255),
             "type": "normal",
             "style": "hatched"},
    }


    Moscow_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # MOSCOW
        "1": {
             "city": "Moscow",
             "color": (217, 43, 44, 255),
             "type": "normal",
             "style": "single"},
        "2": {
             "city": "Moscow",
             "color": (68, 184, 92, 255),
             "type": "normal",
             "style": "single"},
        "3": {
             "city": "Moscow",
             "color": (0, 120, 191, 255),
             "type": "normal",
             "style": "single"},
        "4": {
             "city": "Moscow",
             "color": (25, 193, 243, 255),
             "type": "branch_normal",
             "style": "single"},
        "5": {
             "city": "Moscow",
             "color": (137, 78, 53, 255),
             "type": "circle",
             "style": "single"},
        "6": {
             "city": "Moscow",
             "color": (245, 134, 49, 255),
             "type": "normal",
             "style": "single"},
        "7": {
             "city": "Moscow",
             "color": (142, 71, 156, 255),
             "type": "normal",
             "style": "single"},
        "8": {
             "city": "Moscow",
             "color": (255, 203, 49, 255),
             "type": "normal",
             "style": "single"},
        "8A": {
             "city": "Moscow",
             "color": (255, 203, 49, 255),
             "type": "normal",
             "style": "single"},
        "9": {
             "city": "Moscow",
             "color": (161, 162, 163, 255),
             "type": "normal",
             "style": "single"},
        "10": {
             "city": "Moscow",
             "color": (179, 212, 69, 255),
             "type": "normal",
             "style": "single"},
        "11": {
             "city": "Moscow",
             "color": (121, 205, 205, 255),
             "type": "branch_curve",
             "style": "single"},
        "12": {
             "city": "Moscow",
             "color": (176, 191, 231, 255),
             "type": "normal",
             "style": "single"},
        "14": {
             "city": "Moscow",
             "color": (238, 39, 34, 255),
             "type": "circle",
             "style": "double"},
        "15": {
             "city": "Moscow",
             "color": (222, 100, 161, 255),
             "type": "normal",
             "style": "single"},

        "D1": {
             "city": "Moscow",
             "color": (246, 166, 0, 255),
             "type": "heavy",
             "style": "double"},
        "D2": {
             "city": "Moscow",
             "color": (234, 64, 131, 255),
             "type": "heavy",
             "style": "double"},

        "13": {
             "city": "Moscow",
             "color": (44, 117, 196, 255),
             "type": "monorail",
             "style": "single_thin"},
    }


    Tokyo_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # TOKYO
        "G": {
             "city": "Japan",
             "color": (250, 164, 40, 255),
             "type": "normal",
             "style": "single_thick"},
        "M": {
             "city": "Japan",
             "color": (237, 39, 42, 255),
             "type": "branch",
             "style": "single_thick"},
        "H": {
             "city": "Japan",
             "color": (200, 191, 179, 255),
             "type": "normal",
             "style": "single_thick"},
        "T": {
             "city": "Japan",
             "color": (0, 175, 239, 255),
             "type": "normal",
             "style": "single_thick"},
        "C": {
             "city": "Japan",
             "color": (27, 178, 103, 255),
             "type": "normal",
             "style": "single_thick"},
        "Y": {
             "city": "Japan",
             "color": (210, 167, 99, 255),
             "type": "normal",
             "style": "single_thick"},
        "Z": {
             "city": "Japan",
             "color": (141, 126, 186, 255),
             "type": "normal",
             "style": "single_thick"},
        "N": {
             "city": "Japan",
             "color": (6, 182, 156, 255),
             "type": "normal",
             "style": "single_thick"},
        "F": {
             "city": "Japan",
             "color": (170, 95, 51, 255),
             "type": "normal",
             "style": "single_thick"},
        "A": {
             "city": "Japan",
             "color": (239, 70, 62, 255),
             "type": "normal",
             "style": "single_thick"},
        "I": {
             "city": "Japan",
             "color": (0, 115, 188, 255),
             "type": "normal",
             "style": "single_thick"},
        "S": {
             "city": "Japan",
             "color": (171, 187, 65, 255),
             "type": "normal",
             "style": "single_thick"},
        "E": {
             "city": "Japan",
             "color": (207, 30, 101, 255),
             "type": "normal",
             "style": "single_thick"},

        "JR Yamanote": {
             "city": "Japan",
             "color": (129, 130, 133, 255),
             "type": "circle",
             "style": "single_dashed"},
        "Tokyo Monorail": {
             "city": "Japan",
             "color": (46, 192, 180, 255),
             "type": "monorail",
             "style": "single_thin"},
        "Tokyo Sakura Tram": {
             "city": "Japan",
             "color": (205, 124, 75, 255),
             "type": "tram",
             "style": "single_thin"},
        "Nippori-toneri Liner": {
             "city": "Japan",
             "color": (202, 60, 150, 255),
             "type": "monorail",
             "style": "single_thin"},
    }


    Beijing_style_guide = {
        # --------------------------------------------------------------------------------------------------------------
        # BEIJING
        "1": {
             "city": "Beijing",
             "color": (164, 52, 58, 255),
             "type": "normal",
             "style": "single"},
        "2": {
             "city": "Beijing",
             "color": (0, 75, 135, 255),
             "type": "circle",
             "style": "single"},
        "4": {
             "city": "Beijing",
             "color": (0, 140, 149, 255),
             "type": "normal",
             "style": "single"},
        "5": {
             "city": "Beijing",
             "color": (170, 0, 97, 255),
             "type": "normal",
             "style": "single"},
        "6": {
             "city": "Beijing",
             "color": (181, 133, 0, 255),
             "type": "normal",
             "style": "single"},
        "7": {
             "city": "Beijing",
             "color": (255, 197, 110, 255),
             "type": "normal",
             "style": "single"},
        "8 North": {
             "city": "Beijing",
             "color": (0, 155, 119, 255),
             "type": "half",
             "style": "single"},
        "8 South": {
             "city": "Beijing",
             "color": (0, 155, 119, 255),
             "type": "half",
             "style": "single"},
        "9": {
             "city": "Beijing",
             "color": (151, 215, 0, 255),
             "type": "normal",
             "style": "single"},
        "10": {
             "city": "Beijing",
             "color": (0, 146, 188, 255),
             "type": "circle",
             "style": "single"},
        "13": {
             "city": "Beijing",
             "color": (244, 218, 64, 255),
             "type": "normal",
             "style": "single"},
        "14 West": {
             "city": "Beijing",
             "color": (202, 154, 142, 255),
             "type": "half",
             "style": "single"},
        "14 East": {
             "city": "Beijing",
             "color": (202, 154, 142, 255),
             "type": "half",
             "style": "single"},
        "15": {
             "city": "Beijing",
             "color": (101, 50, 121, 255),
             "type": "normal",
             "style": "single"},
        "16": {
             "city": "Beijing",
             "color": (107, 165, 57, 255),
             "type": "normal",
             "style": "single"},

        "Yizhuang": {
             "city": "Beijing",
             "color": (208, 0, 111, 255),
             "type": "exterior",
             "style": "single"},
        "Fangshan": {
             "city": "Beijing",
             "color": (216, 96, 24, 255),
             "type": "exterior",
             "style": "single"},
        "Yanfang": {
             "city": "Beijing",
             "color": (216, 96, 24, 255),
             "type": "exterior",
             "style": "single"},
        "S1": {
             "city": "Beijing",
             "color": (164, 90, 42, 255),
             "type": "exterior",
             "style": "single"},
        "Changping": {
             "city": "Beijing",
             "color": (217, 134, 186, 255),
             "type": "exterior",
             "style": "single"},
        "Capital Airport": {
             "city": "Beijing",
             "color": (161, 146, 178, 255),
             "type": "shuttle",
             "style": "single"},
        "Daxing Airport": {
             "city": "Beijing",
             "color": (0, 73, 165, 255),
             "type": "shuttle",
             "style": "single"},
        "Xijiao": {
             "city": "Beijing",
             "color": (210, 38, 48, 255),
             "type": "light",
             "style": "single"},
        "Yizhuang T1": {
             "city": "Beijing",
             "color": (210, 38, 48, 255),
             "type": "light",
             "style": "single"},
    }
