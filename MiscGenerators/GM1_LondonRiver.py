import random
import numpy as np

import style_data as sd
import geometric_elements as ge
import Map as map

curve_scale = 50
curve_scale = curve_scale * sd.StyleDatabase.t_scale
ftc_dict = {"up": {"type": 90, "orientation": 0, "chirality": "L", "transform": (curve_scale, -1*curve_scale)},
            "down": {"type": 90, "orientation": 0, "chirality": "R", "transform": (curve_scale, curve_scale)},
            "dxup": {"type": 45, "orientation": 0, "chirality": "Ls", "transform": (2*curve_scale, -1*curve_scale)},
            "dxdn": {"type": 45, "orientation": 0, "chirality": "Rs", "transform": (2*curve_scale, curve_scale)}}
ctf_dict = {"up": {"type": 90, "orientation": 90, "chirality": "R", "transform": (curve_scale, -1*curve_scale)},
            "down": {"type": 90, "orientation": 270, "chirality": "L", "transform": (curve_scale, curve_scale)},
            "dxup": {"type": 45, "orientation": 90, "chirality": "Rd", "transform": (2*curve_scale, -1*curve_scale)},
            "dxdn": {"type": 45, "orientation": 270, "chirality": "Ld", "transform": (2*curve_scale, curve_scale)}}


class GM1_LondonRiver:
    def __init__(self, xs, ys, map):
        self.render_list = []
        self.xs = xs
        self.ys = ys
        self.map = map

    def generate(self):
        # Pick starting location
        starting_location = (0, random.randint(int(self.ys / 2), int(3 * self.ys / 4)))
        current_location = starting_location

        current_location = self.step_flat(current_location)

        run_course = False
        while run_course is False:
            current_dir = np.random.choice(["up", "dxup", "dxdn", "down"], p=[0.35, 0.15, 0.15, 0.35])
            hold_location = current_location
            current_location = self.joint_ftc(current_location, current_dir)
            current_location = self.step_climb(current_location, current_dir)
            if current_location[1] >= self.ys*7/8 or current_location[1] <= self.ys/2:
                trash = self.render_list.pop()
                trash = self.render_list.pop()
                current_location = hold_location
                continue
            current_location = self.joint_ctf(current_location, current_dir)
            current_location = self.step_flat(current_location)
            if current_location[0] >= int(self.xs*99/100):
                run_course = True

        return self.render_list

    def step_flat(self, cur_l):
        next_distance = random.randint(int(self.xs / 20), int(self.xs / 6))
        next_l = (cur_l[0] + next_distance, cur_l[1])
        self.render_list.append(ge.Segment(loc1=cur_l, loc2=next_l, orientation=0))
        return next_l

    def joint_ftc(self, cur_l, dir):
        next_l = (cur_l[0] + ftc_dict[dir]["transform"][0], cur_l[1] + ftc_dict[dir]["transform"][1])
        self.render_list.append(ge.arc_builder(arc_type=ftc_dict[dir]["type"],
                                               loc1=cur_l, loc2=next_l,
                                               orientation=ftc_dict[dir]["orientation"],
                                               chirality=ftc_dict[dir]["chirality"],
                                               curve_scale=curve_scale))
        return next_l

    def step_climb(self, cur_l, current_dir):
        if current_dir == "up" or current_dir == "down":
            next_distance = random.randint(int(self.ys / 14), int(self.ys / 6))
            if current_dir == "up":
                next_l = (cur_l[0], cur_l[1] - next_distance)
                self.render_list.append(ge.Segment(loc1=cur_l, loc2=next_l, orientation=90))
            elif current_dir == "down":
                next_l = (cur_l[0], cur_l[1] + next_distance)
                self.render_list.append(ge.Segment(loc1=cur_l, loc2=next_l, orientation=270))
        elif current_dir == "dxup" or current_dir == "dxdn":
            next_distance = random.randint(int(self.ys / 14), int(self.ys / 6))
            if current_dir == "dxup":
                next_l = (cur_l[0] + next_distance, cur_l[1] - next_distance)
                self.render_list.append(ge.Segment(loc1=cur_l, loc2=next_l, orientation=45))
            elif current_dir == "dxdn":
                next_l = (cur_l[0] + next_distance, cur_l[1] + next_distance)
                self.render_list.append(ge.Segment(loc1=cur_l, loc2=next_l, orientation=315))
        return next_l

    def joint_ctf(self, cur_l, dir):
        next_l = (cur_l[0] + ftc_dict[dir]["transform"][0], cur_l[1] + ftc_dict[dir]["transform"][1])
        self.render_list.append(ge.arc_builder(arc_type=ctf_dict[dir]["type"],
                                               loc1=cur_l, loc2=next_l,
                                               orientation=ctf_dict[dir]["orientation"],
                                               chirality=ctf_dict[dir]["chirality"],
                                               curve_scale=curve_scale))
        return next_l




