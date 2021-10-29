import numpy as np

from map_lib import Feature
from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.TrackGeometry import Straight, Arc
from geometry_lib.SpecialGeometry import TextBox

from options import prime as opt
from parameters.StyleGuides import complete_style_guide as csg


def gRiver():
    river = Feature.Feature('River')

    # Pick river starting location
    starting_ys = np.random.randint(int(csg.ys * opt.b_river_ys[0]), int(csg.ys * opt.b_river_ys[1]))
    starting_location = Spatial(x=0, y=starting_ys, o=degree(0))

    # Generate the river
    error, completed_piece_list = river_step(piece_list=[], current_location=starting_location, csg=csg)
    river.render_list = completed_piece_list

    # Apply text label
    possible_segments = []
    for seg in river.render_list:
        if type(seg) == Straight and seg.spatial1.o == 0 and seg.spatial2.x - seg.spatial1.x > 400 * opt.s:
            possible_segments.append(seg)
    possible_segments.pop() # Because the last segment can hang off the map, don't place text in it ever
    chosen_segment = np.random.choice(possible_segments)
    chosen_position_x = np.random.randint(int(chosen_segment.spatial1.x) + 100 * opt.s, int(chosen_segment.spatial2.x) - 300 * opt.s)
    text_location = Spatial(x=chosen_position_x, y=chosen_segment.spatial1.y, o=degree(0))

    text_box = TextBox(spatial_station=text_location, text="River Thames", offset=0,
                       font_name="fonts/ITC - JohnstonITCPro-Medium.otf", font_size=opt.river_label_font_size)
    river.label_list.append(text_box)

    return river


def river_step(piece_list, current_location: Spatial, csg):
    attempts = 100
    while attempts > 0:
        # Generate a package
        if current_location.x == 0:
            next_length = np.random.randint(opt.lb_flat[0] + 300, opt.lb_flat[1])
        elif current_location.o == 0:
            next_length = np.random.randint(opt.lb_flat[0], opt.lb_flat[1])
        else:
            next_length = np.random.randint(opt.lb_other[0], opt.lb_other[1])
        next_segment = Straight(spatial1=current_location, distance=next_length)
        if current_location.o == 0:
            next_dir_change = np.random.choice(opt.v_river_change, p=opt.p_river_change)
        else:
            next_dir_change = next_segment.spatial2.o.change_to_0
        next_curve = Arc(spatial1=next_segment.spatial2, arc_angle_change=next_dir_change, curve_radius=opt.cr_river)

        # If the package is off the right end of the map
        if next_segment.spatial2.x > csg.xs:
            if next_segment.spatial2.o == 0:
                piece_list.append(next_segment)
                return None, piece_list
            else:
                attempts -= 1
                continue

        if next_curve.spatial2.y > csg.ys * opt.b_river_ys[1] or \
                next_curve.spatial2.y < csg.ys * opt.b_river_ys[0] or \
                next_curve.spatial2.x > csg.xs * 0.95:
            attempts -= 1
            continue

        error, new_piece_list = river_step(piece_list + [next_segment, next_curve], next_curve.spatial2, csg)
        if error is None:
            return None, new_piece_list
        else:
            attempts -= 1
            continue

    return "error", piece_list





