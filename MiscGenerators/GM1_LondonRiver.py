import math
import random
import numpy as np

import geometric_elements as ge
from Maps import M1_London as map

class GM1_LondonRiver:
    def __init__(self, xgs, ygs, map):
        self.render_list = []
        self.xgs = xgs
        self.ygs = ygs
        self.map = map

    def generate(self):
        # Pick starting location
        starting_location = (0, random.randint(int(self.ygs/2), int(3*self.ygs/4)))
        current_location = starting_location

        current_location = self.step_flat(current_location)

        run_course = False
        while run_course is False:
            current_dir = np.random.choice(["up", "dxup", "dxdn", "down"], p=[0.35, 0.35, 0.15, 0.15])
            hold_location = current_location
            current_location = self.joint_ftc(current_location, current_dir)
            current_location = self.step_climb(current_location, current_dir)
            if current_location[1] >= self.ygs*7/8 or current_location[1] <= self.ygs/2:
                trash = self.render_list.pop()
                trash = self.render_list.pop()
                current_location = hold_location
                continue
            current_location = self.joint_ctf(current_location, current_dir)
            current_location = self.step_flat(current_location)
            if current_location[0] >= self.xgs:
                run_course = True

        return self.render_list

    def step_flat(self, cur_l):
        next_distance = random.randint(int(self.xgs/20), int(self.xgs/10))
        next_l = (cur_l[0] + next_distance, cur_l[1])
        self.render_list.append(ge.Segment(style="LondonRiver", loc1=cur_l, loc2=next_l, orientation=0))
        for x_pos in range(cur_l[0], next_l[0]+1):
            self.map.collision_array[x_pos, cur_l[1]] = map.IntersectNode("River", 0)
        return next_l

    def joint_ftc(self, cur_l, dir_change):
        if dir_change == "up":
            next_l = (cur_l[0] + 1, cur_l[1] - 1)
            self.render_list.append(ge.Arc90(style="LondonRiver", loc1=cur_l,
                                             orientation=0, chirality='L'))
            self.map.collision_array[cur_l[0], cur_l[1]] = map.IntersectNode("River", 0)
            self.map.collision_array[next_l[0], next_l[1]] = map.IntersectNode("River", 90)
        elif dir_change == "down":
            next_l = (cur_l[0] + 1, cur_l[1] + 1)
            self.render_list.append(ge.Arc90(style="LondonRiver", loc1=cur_l,
                                             orientation=0, chirality='R'))
            self.map.collision_array[cur_l[0], cur_l[1]] = map.IntersectNode("River", 0)
            self.map.collision_array[next_l[0], next_l[1]] = map.IntersectNode("River", 270)
        elif dir_change == "dxup":
            next_l = (cur_l[0] + 2, cur_l[1] - 1)
            self.render_list.append(ge.Arc45(style="LondonRiver", loc1=cur_l, loc2=next_l,
                                             orientation=0, chirality='Ls'))
            self.map.collision_array[cur_l[0], cur_l[1]] = map.IntersectNode("River", 0)
            self.map.collision_array[next_l[0], next_l[1]] = map.IntersectNode("River", 45)
        elif dir_change == "dxdn":
            next_l = (cur_l[0] + 2, cur_l[1] + 1)
            self.render_list.append(ge.Arc45(style="LondonRiver", loc1=cur_l, loc2=next_l,
                                             orientation=0, chirality='Rs'))
            self.map.collision_array[cur_l[0], cur_l[1]] = map.IntersectNode("River", 0)
            self.map.collision_array[next_l[0], next_l[1]] = map.IntersectNode("River", 315)
        return next_l

    def step_climb(self, cur_l, current_dir):
        if current_dir == "up" or current_dir == "down":
            next_distance = random.randint(int(self.ygs/14), int(self.ygs/6))
            if current_dir == "up":
                next_l = (cur_l[0], cur_l[1] - next_distance)
                self.render_list.append(ge.Segment(style="LondonRiver", loc1=cur_l, loc2=next_l, orientation=90))
                for y_pos in range(cur_l[1], next_l[1] + 1):
                    self.map.collision_array[cur_l[0], y_pos] = map.IntersectNode("River", 90)
            elif current_dir == "down":
                next_l = (cur_l[0], cur_l[1] + next_distance)
                self.render_list.append(ge.Segment(style="LondonRiver", loc1=cur_l, loc2=next_l, orientation=270))
        elif current_dir == "dxup" or current_dir == "dxdn":
            next_distance = random.randint(int(self.ygs/10), int(self.ygs/4))
            if current_dir == "dxup":
                next_l = (cur_l[0] + next_distance, cur_l[1] - next_distance)
                self.render_list.append(ge.Segment(style="LondonRiver", loc1=cur_l, loc2=next_l, orientation=45))
            elif current_dir == "dxdn":
                next_l = (cur_l[0] + next_distance, cur_l[1] + next_distance)
                self.render_list.append(ge.Segment(style="LondonRiver", loc1=cur_l, loc2=next_l, orientation=315))
        return next_l

    def joint_ctf(self, cur_l, dir_change):
        if dir_change == "up":
            next_l = (cur_l[0] + 1, cur_l[1] - 1)
            self.render_list.append(ge.Arc90(style="LondonRiver", loc1=cur_l,
                                             orientation=90, chirality='R'))
        elif dir_change == "down":
            next_l = (cur_l[0] + 1, cur_l[1] + 1)
            self.render_list.append(ge.Arc90(style="LondonRiver", loc1=cur_l,
                                             orientation=270, chirality='L'))
        elif dir_change == "dxup":
            next_l = (cur_l[0] + 2, cur_l[1] - 1)
            self.render_list.append(ge.Arc45(style="LondonRiver", loc1=cur_l, loc2=next_l,
                                             orientation=90, chirality='Rd'))
        elif dir_change == "dxdn":
            next_l = (cur_l[0] + 2, cur_l[1] + 1)
            self.render_list.append(ge.Arc45(style="LondonRiver", loc1=cur_l, loc2=next_l,
                                             orientation=270, chirality='Ld'))
        return next_l




