import random
import numpy as np
import Map


class G2_TransitMapv2:
    def __init__(self, size, gparams):
        self.map = Map.Map()
        self.size = size
        self.gparams = gparams
        random.seed()

    @property
    def generate(self):
        xs = self.size[0]
        ys = self.size[1]



        line_list = []
        branch_list = []
        random.shuffle(style_guide)

        # Initial pull from style, FOR EACH LINE
        for n in range(1, len(style_guide)+1):
            this_style = style_guide.pop()
            line_list.append({"id": n,
                              "color": this_style["color"],
                              "type": this_style["type"],
                              "style": this_style["style"]})

        # Location and direction generation, FOR EACH LINE
        for line in line_list:
            line["starting_loc"] = np.array([random.randint(xs*0.35, xs-xs*0.35), random.randint(ys*0.35, ys-ys*0.35)])
            line["starting_dir"] = Direction(random.randint(1, 8))

        def step(c_loc, c_dir):
            next_distance = random.randint(40, 200)
            if line["type"] == "light":
                next_distance = next_distance/2
            nonlocal termination_score
            termination_score -= next_distance * random.randint(1, 10)
            if termination_score < 0:
                return 1, None
            next_vector = np.multiply(next_distance, c_dir.get_dirv()).astype(int)
            next_loc_i = np.add(c_loc, next_vector)
            if (next_loc_i[0] > xs * 0.95) | (next_loc_i[0] < xs * 0.05):
                return 1, None
            elif (next_loc_i[1] > xs * 0.95) | (next_loc_i[1] < xs * 0.05):
                return 1, None
            return 0, next_loc_i

        # Spline generation, FOR EACH LINE
        for line in line_list:
            # Initial setup
            coord_list = []
            has_reversed = False
            line_trend = line["starting_dir"].get_diri()
            coord_list.append(tuple(line["starting_loc"]))
            termination_score = xs * 3
            if line["type"] == "shuttle":
                termination_score = xs / 1
            elif line["type"] == "cable":
                termination_score = xs / 2
            elif line["type"] == "heavy":
                termination_score = xs * 5
            elif line["type"] == "circle":
                termination_score = xs * 4

            current_loc = line["starting_loc"]
            current_dir = Direction(line["starting_dir"].get_diri())

            proceed, next_loc = step(current_loc, current_dir)
            if not proceed:
                coord_list.append(tuple(next_loc))
                if line["type"] == "heavy":
                    x = [0.10, 0.90]
                elif line["type"] == "light":
                    x = [0.25, 0.75]
                elif line["type"] == "circle":
                    x = [0, 1]
                else:
                    x = [0.05, 0.95]
                if np.random.choice([True, False], p=x):
                    branch_list.append({"id": "branch",
                                        "color": line["color"],
                                        "type": line["type"],
                                        "style": line["style"],
                                        "starting_loc": next_loc,
                                        "starting_dir": Direction(current_dir.get_diri())})
                current_loc = next_loc
            if proceed:
                pass

            while True:
                # Check for change
                if np.random.choice([True, False], p=[0.5, 0.5]):
                    change_dir = np.random.choice([-1, 0, 1])
                    diff = current_dir.get_diff(line_trend, current_dir.get_diri() + change_dir)
                    if line["type"] == "circle":
                        if np.random.choice([True, False], p=[0.9, 0.1]):
                            current_dir.change_direction(1)
                        else:
                            current_dir.change_direction(change_dir)
                    elif abs(diff) <= 1:
                        current_dir.change_direction(change_dir)
                    else:
                        if line["type"] == "heavy":
                            current_dir.change_direction(change_dir)
                        elif np.random.choice([True, False], p=[0.2, 0.8]):
                            current_dir.change_direction(change_dir)
                else:
                    pass

                # Next step
                proceed, next_loc = step(current_loc, current_dir)
                if not proceed:
                    coord_list.append(tuple(next_loc))
                    if line["type"] == "heavy":
                        x = [0.10, 0.90]
                    elif line["type"] == "light":
                        x = [0.25, 0.75]
                    elif line["type"] == "circle":
                        x = [0, 1]
                    else:
                        x = [0.05, 0.95]
                    if np.random.choice([True, False], p=x):
                        branch_list.append({"id": "branch",
                              "color": line["color"],
                              "type": line["type"],
                              "style": line["style"],
                              "starting_loc": next_loc,
                              "starting_dir": Direction(current_dir.get_diri())})
                    current_loc = next_loc
                elif proceed and line["type"] == "light":
                    break
                elif proceed and has_reversed:
                    break
                elif proceed:
                    has_reversed = True
                    current_dir.reverse_direction()
                    coord_list.reverse()
                    termination_score = xs * 3
                    if line["type"] == "shuttle":
                        termination_score = xs / 1
                    elif line["type"] == "cable":
                        termination_score = xs / 2
                    elif line["type"] == "heavy":
                        termination_score = xs * 5
                    elif line["type"] == "circle":
                        termination_score = xs * 4
                    current_loc = line["starting_loc"]
                    if line_trend > 4:
                        line_trend -= 4
                    else:
                        line_trend += 4

            line["coords"] = coord_list

        # Branch generation
        for line in branch_list:
            # Initial setup
            coord_list = []
            has_reversed = False
            line_trend = line["starting_dir"].get_diri()
            coord_list.append(tuple(line["starting_loc"]))
            termination_score = xs * 3
            if line["type"] == "shuttle":
                termination_score = xs / 1
            elif line["type"] == "cable":
                termination_score = xs / 2

            current_loc = line["starting_loc"]
            current_dir = Direction(line["starting_dir"].get_diri())

            proceed, next_loc = step(current_loc, current_dir)
            if not proceed:
                coord_list.append(tuple(next_loc))
                current_loc = next_loc
            if proceed:
                pass

            while True:
                # Check for change
                if np.random.choice([True, False], p=[0.5, 0.5]):
                    change_dir = np.random.choice([-1, 0, 1])
                    diff = current_dir.get_diff(line_trend, current_dir.get_diri() + change_dir)
                    if line["type"] == "circle":
                        if np.random.choice([True, False], p=[0.9, 0.1]):
                            current_dir.change_direction(1)
                        else:
                            current_dir.change_direction(change_dir)
                    elif abs(diff) <= 1:
                        current_dir.change_direction(change_dir)
                    else:
                        if line["type"] == "heavy":
                            current_dir.change_direction(change_dir)
                        elif np.random.choice([True, False], p=[0.2, 0.8]):
                            current_dir.change_direction(change_dir)
                else:
                    pass

                # Next step
                proceed, next_loc = step(current_loc, current_dir)
                if not proceed:
                    coord_list.append(tuple(next_loc))
                    current_loc = next_loc
                elif proceed:
                    break

            line["coords"] = coord_list


        # Export
        for line in line_list:
            self.map.add_line(line["color"], line["style"], line["coords"])
        for line in branch_list:
            self.map.add_line(line["color"], line["style"], line["coords"])

        return self.map

    def gen_features(self, map2):
        river_segs = [np.array([0, 1]),
                      np.array([np.sqrt(0.5), np.sqrt(0.5)]),
                      np.array([1, 0]),
                      np.array([np.sqrt(0.5), -1 * np.sqrt(0.5)]),
                      np.array([0, -1])]

        # Origin of the river
        xs = self.size[0]
        ys = self.size[1]
        river_coords = []

        river_org_x = 0
        river_org_y = random.randint(int(ys/3*2), ys-100)
        river_coords.append(np.array([river_org_x, river_org_y]))
        cur_loc = np.array([river_org_x, river_org_y])

        def next_direc(d):
            if d == 1:
                return np.random.choice([2, 3], p=[0.2, 0.8])
            elif d == 2:
                return np.random.choice([1, 3], p=[0.4, 0.6])
            elif d == 3:
                return np.random.choice([1, 2, 4, 5], p=[0.4, 0.1, 0.1, 0.4])
            elif d == 4:
                return np.random.choice([3, 5], p=[0.6, 0.4])
            elif d == 5:
                return np.random.choice([3, 4], p=[0.8, 0.2])

        direc = 3
        while cur_loc[0] < 2000:
            dis = random.randint(int(xs / 10), int(xs / 5))
            vec = np.multiply(dis, river_segs[direc-1])
            direc = next_direc(direc)
            next_loc = np.add(cur_loc, vec)
            if (next_loc[1] > ys-100) | (next_loc[1] < int(ys/2)):
                continue
            river_coords.append(next_loc)
            cur_loc = next_loc

        if river_coords[-1][0] < xs:
            river_coords.append(np.array(xs, river_coords[-1][1]))

        river_tuples = []
        for coords in river_coords:
            river_tuples.append(tuple(coords))

        map2.add_feature("river", river_tuples)
        return map2




class Direction:
    direction_dict = {1: np.array([1, 0]),
                      2: np.array([np.sqrt(0.5), np.sqrt(0.5)]),
                      3: np.array([0, 1]),
                      4: np.array([-1*np.sqrt(0.5), np.sqrt(0.5)]),
                      5: np.array([-1, 0]),
                      6: np.array([-1*np.sqrt(0.5), -1*np.sqrt(0.5)]),
                      7: np.array([0, -1]),
                      8: np.array([np.sqrt(0.5), -1*np.sqrt(0.5)])}

    def __init__(self, dirt):
        self.direction = dirt
        if dirt > 4:
            self.reverse_dir = dirt-4
        elif dirt <= 4:
            self.reverse_dir = dirt+4

    def get_dirv(self):
        return Direction.direction_dict[self.direction]

    def get_diri(self):
        return self.direction

    def get_diff(self, f, t):
        diff = abs(t - f)
        if abs(diff) > 4:
            diff = -1 * (8 - diff)
        return diff

    def change_direction(self, change):
        self.direction += change
        if self.direction == 9:
            self.direction = 1
        elif self.direction == 0:
            self.direction = 8

    def reverse_direction(self):
        self.direction = self.reverse_dir

        






