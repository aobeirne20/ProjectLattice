import random
import numpy as np
import Graph


class G1_TransitMap:
    def __init__(self, size, gparams):
        self.graph = Graph.Graph()
        self.size = size
        self.gparams = gparams
        random.seed()

    def generate(self):
        xs = self.size[0]
        ys = self.size[1]
        num_lines = np.random.choice([9, 10, 11, 12, 13], p=[0.1, 0.2, 0.4, 0.2, 0.1])

        line_color_codes = [(178, 99, 0, 255), (220, 36, 31, 255), (255, 211, 41, 255), (0, 125, 50, 255),
                            (244, 169, 190, 255), (161, 165, 167, 255), (155, 0, 88, 255), (0, 0, 0, 255),
                            (0, 25, 168, 255), (0, 152, 216, 255), (147, 206, 186, 255)]
        random.shuffle(line_color_codes)
        num_lines = 11

        line_list = []
        for n in range(1, num_lines+1):
            is_circular = np.random.choice([True, False], p=[0.0909, 0.9091])
            is_shuttle = np.random.choice([True, False], p=[0.0909, 0.9091])
            line_list.append(Line(n, line_color_codes.pop(), is_circular, is_shuttle))

        vert_segs = []
        horz_segs = []
        dxup_segs = []
        dxdn_segs = []

        for line in line_list:
            line.direction.random_direction()
            line.starting_direction = line.direction

            # Pick starting location
            line.starting_loc = [random.randint(xs*0.25, xs-xs*0.25), random.randint(ys*0.25, ys-ys*0.25)]
            current_loc = line.starting_loc
            termination_chance = 0
            change_counter = 0
            has_flipped = False
            flip_now = False

            while True:
                distance = random.randint(20, 100)
                if flip_now:
                    line.flip_line()
                    line.starting_direction.flip_direction()
                    line.direction = line.starting_direction

                    current_loc = line.starting_loc
                    termination_chance = 0;
                    flip_now = False
                else:
                    change_val = np.random.choice([-1, 0, 1], p=[0.1, 0.8, 0.1])
                    if change_val != 0 & change_counter <= 0:
                        change_counter = random.randint(60, 200)
                        line.direction.change_direction(change_val)
                    elif change_val == 0:
                        change_counter -= distance

                travel = list(np.multiply(line.direction.give_dir(),distance))
                travel2 = [int(x) for x in travel]
                next_loc = list(np.add(current_loc, travel2))

                termination_chance = termination_chance + int(random.randint(1, 3) * distance / 20)
                if termination_chance > 100:
                    if has_flipped:
                        break
                    else:
                        has_flipped = True
                        flip_now = True
                        pass

                if next_loc[0] > int(self.size[0]*0.90) | next_loc[0] < int(self.size[0]*0.10):
                    if has_flipped:
                        break
                    else:
                        has_flipped = True
                        flip_now = True
                        pass

                if next_loc[1] > int(self.size[1]*0.90) | next_loc[1] < int(self.size[1]*0.10):
                    if has_flipped:
                        break
                    else:
                        has_flipped = True
                        flip_now = True
                        pass

                line.add_spline(current_loc, next_loc)
                self.graph.add_edge(line.color_code, current_loc, next_loc)
                # Horizontal
                if line.direction.direction == 1 | line.direction.direction == 5:
                    horz_segs.append([current_loc, next_loc])

                # Dxup
                elif line.direction.direction == 2 | line.direction.direction == 6:
                    dxup_segs.append([current_loc, next_loc])

                # Vertical
                elif line.direction.direction == 3 | line.direction.direction == 7:
                    vert_segs.append([current_loc, next_loc])

                # Dxdown
                elif line.direction.direction == 4 | line.direction.direction == 8:
                    dxdn_segs.append([current_loc, next_loc])

                current_loc = next_loc


        return self.graph


class Line:
    def __init__(self, ID, color, is_circular, is_shuttle):
        self.ID = ID
        self.color_code = color
        self.complexity = random.randint(50, 150)
        self.is_circular = is_circular
        self.is_shuttle = is_shuttle
        self.spline = []
        self.direction = Direction()
        self.starting_loc = None
        self.starting_direction = None

    def add_spline(self, loc1, loc2):
        self.spline.append((loc1, loc2))

    def flip_line(self):
        self.spline.reverse()

class Direction:
    def __init__(self):
        self.direction = None
        self.direction_dict = {1:(1,0), 2:(0.7071, 0.7071), 3:(0, 1), 4:(-0.7071, 0.7071),
                               5:(-1, 0), 6:(-0.7071, -0.7071), 7:(0, -1), 8:(0.7071, -0.7071)}

    def give_dir(self):
        return self.direction_dict[self.direction]

    def random_direction(self):
        self.direction = random.randint(1, 8)

    def change_direction(self, change):
        self.direction += change
        if self.direction == 9:
            self.direction = 1
        elif self.direction == 0:
            self.direction = 8

    def flip_direction(self):
        if self.direction == 1:
            self.direction = 5
        elif self.direction == 2:
            self.direction = 6
        elif self.direction == 3:
            self.direction = 7
        elif self.direction == 4:
            self.direction = 8
        elif self.direction == 5:
            self.direction = 1
        elif self.direction == 6:
            self.direction = 2
        elif self.direction == 7:
            self.direction = 3
        elif self.direction == 8:
            self.direction = 4
















