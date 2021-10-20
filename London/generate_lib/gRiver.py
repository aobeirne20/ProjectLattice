import numpy as np

from map_lib import Feature
from CompleteStyleGuide import CompleteStyleGuide
from geometry_lib.Spatial import Spatial
from geometry_lib.degree import degree
from geometry_lib.TrackGeometry import Straight, Arc
from options import prime as opt


def gRiver(csg: CompleteStyleGuide):
    river = Feature.Feature()

    # Pick river starting location
    starting_ys = np.random.randint(int(csg.ys * opt.b_river_ys[0]), int(csg.ys * opt.b_river_ys[1]))
    starting_location = Spatial(x=0, y=starting_ys, o=degree(0))

    error, completed_piece_list = river_step(piece_list=[], current_location=starting_location, csg=csg)
    river.render_list = completed_piece_list

    return river


def river_step(piece_list, current_location: Spatial, csg):
    attempts = 100
    while attempts > 0:
        # Generate a package
        if current_location.o == 0:
            next_length = np.random.randint(opt.s * opt.lb_flat[0], opt.s * opt.lb_flat[1])
        else:
            next_length = np.random.randint(opt.s * opt.lb_other[0], opt.s * opt.lb_other[1])
        next_segment = Straight(spatial1=current_location, distance=next_length)
        if current_location.o == 0:
            next_dir_change = np.random.choice([-2, -1, 1, 2], p=opt.p_river_change_n90_n45_45_90)
        else:
            next_dir_change = next_segment.spatial2.o.change_to_0
        next_curve = Arc(spatial1=next_segment.spatial2, arc_angle_change=next_dir_change, curve_radius=opt.cr_river * opt.s)

        # If the package is off the right end of the map
        if next_segment.spatial2.x > csg.xs:
            piece_list.append(next_segment)
            return None, piece_list

        if next_curve.spatial2.y > csg.ys * opt.b_river_ys[1] or next_curve.spatial2.y < csg.ys * opt.b_river_ys[0]:
            attempts -= 1
            continue

        error, new_piece_list = river_step(piece_list + [next_segment, next_curve], next_curve.spatial2, csg)
        if error is None:
            return None, new_piece_list
        else:
            attempts -= 1
            continue

    return "error", piece_list





